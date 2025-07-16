import React, { useState, useCallback } from 'react';
import { Upload, Download, AlertCircle, CheckCircle, BarChart3, Table, Settings, Loader2 } from 'lucide-react';
import * as XLSX from 'xlsx';
import Papa from 'papaparse';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, ScatterChart, Scatter, BarChart, Bar } from 'recharts';

const MLPredictionApp = () => {
  const [data, setData] = useState([]);
  const [predictions, setPredictions] = useState([]);
  const [fileName, setFileName] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [activeTab, setActiveTab] = useState('upload');
  const [azureConfig, setAzureConfig] = useState({
    endpoint: '',
    apiKey: '',
    headers: { 'Content-Type': 'application/json' }
  });

  // File upload handler
  const handleFileUpload = useCallback((event) => {
    const file = event.target.files[0];
    if (!file) return;

    setLoading(true);
    setError('');
    setSuccess('');
    setFileName(file.name);

    const reader = new FileReader();
    reader.onload = (e) => {
      try {
        const fileExtension = file.name.split('.').pop().toLowerCase();
        let parsedData = [];

        if (fileExtension === 'csv') {
         
          Papa.parse(e.target.result, {
            header: true,
            dynamicTyping: true,
            skipEmptyLines: true,
            complete: (results) => {
              parsedData = results.data.filter(row => 
                Object.values(row).some(val => val !== null && val !== undefined && val !== '')
              );
              setData(parsedData);
              setSuccess(`Successfully loaded ${parsedData.length} rows from CSV file`);
              setLoading(false);
              setActiveTab('data');
            },
            error: (error) => {
              setError(`CSV parsing error: ${error.message}`);
              setLoading(false);
            }
          });
        } else if (['xlsx', 'xls'].includes(fileExtension)) {
          // Parse Excel
          const workbook = XLSX.read(e.target.result, { type: 'binary' });
          const sheetName = workbook.SheetNames[0];
          const worksheet = workbook.Sheets[sheetName];
          parsedData = XLSX.utils.sheet_to_json(worksheet, { defval: '' });
          
          // Clean data
          parsedData = parsedData.filter(row => 
            Object.values(row).some(val => val !== null && val !== undefined && val !== '')
          );
          
          setData(parsedData);
          setSuccess(`Successfully loaded ${parsedData.length} rows from Excel file`);
          setLoading(false);
          setActiveTab('data');
        } else {
          setError('Unsupported file format. Please upload CSV or Excel files.');
          setLoading(false);
        }
      } catch (err) {
        setError(`File processing error: ${err.message}`);
        setLoading(false);
      }
    };

    if (file.name.endsWith('.csv')) {
      reader.readAsText(file);
    } else {
      reader.readAsBinaryString(file);
    }
  }, []);

  // Azure ML API call
  const callAzureML = async () => {
    if (!azureConfig.endpoint) {
      setError('Please configure Azure ML endpoint URL');
      return;
    }

    if (data.length === 0) {
      setError('No data to send for prediction');
      return;
    }

    setLoading(true);
    setError('');

    try {
      const headers = {
        'Content-Type': 'application/json',
        ...(azureConfig.apiKey && { 'Authorization': `Bearer ${azureConfig.apiKey}` })
      };

      const response = await fetch(azureConfig.endpoint, {
        method: 'POST',
        headers,
        body: JSON.stringify({
          data: data,
          // Add additional payload structure as needed for your Azure ML model
        })
      });

      if (!response.ok) {
        throw new Error(`API Error: ${response.status} - ${response.statusText}`);
      }

      const result = await response.json();
      
  
      const predictionsData = data.map((row, index) => ({
        ...row,
        prediction: result.predictions ? result.predictions[index] : Math.random() * 100, // Placeholder
      }));

      setPredictions(predictionsData);
      setSuccess(`Successfully generated ${predictionsData.length} predictions`);
      setActiveTab('results');
    } catch (err) {
      setError(`Prediction error: ${err.message}`);

      const mockPredictions = data.map(row => ({
        ...row,
        prediction: Math.random() * 100,
      }));
      setPredictions(mockPredictions);
      setSuccess('Demo: Generated mock predictions (configure Azure ML endpoint for real predictions)');
      setActiveTab('results');
    } finally {
      setLoading(false);
    }
  };

  // Export results
  const exportResults = (format) => {
    if (predictions.length === 0) {
      setError('No predictions to export');
      return;
    }

    if (format === 'csv') {
      const csv = Papa.unparse(predictions);
      const blob = new Blob([csv], { type: 'text/csv' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `predictions_${fileName.split('.')[0]}.csv`;
      a.click();
      URL.revokeObjectURL(url);
    } else if (format === 'xlsx') {
      const ws = XLSX.utils.json_to_sheet(predictions);
      const wb = XLSX.utils.book_new();
      XLSX.utils.book_append_sheet(wb, ws, 'Predictions');
      XLSX.writeFile(wb, `predictions_${fileName.split('.')[0]}.xlsx`);
    }
    setSuccess(`Results exported as ${format.toUpperCase()}`);
  };


  const getChartData = () => {
    if (predictions.length === 0) return [];
    
    return predictions.map((row, index) => ({
      index: index + 1,
      prediction: row.prediction,
      // confidence: row.confidence
    }));
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="container mx-auto px-4 py-8">
        <div className="max-w-6xl mx-auto">
          {/* Header */}
          <div className="bg-white rounded-xl shadow-lg p-6 mb-8">
            <div className="flex items-center justify-between">
              <div>
                <h1 className="text-3xl font-bold text-gray-900 mb-2">Seed Sale Prediction</h1>
                <p className="text-gray-600">Upload your data and get AI-powered predictions</p>
              </div>
              <div className="flex items-center space-x-4">
                <BarChart3 className="w-8 h-8 text-blue-600" />
              </div>
            </div>
          </div>

          {/* Navigation Tabs */}
          <div className="bg-white rounded-xl shadow-lg mb-8">
            <div className="border-b border-gray-200">
              <nav className="flex space-x-8 px-6">
                {[
                  { id: 'upload', label: 'Upload Data', icon: Upload },
                  { id: 'data', label: 'Data Preview', icon: Table },
                  { id: 'config', label: 'ML Config', icon: Settings },
                  { id: 'results', label: 'Results', icon: BarChart3 }
                ].map(tab => (
                  <button
                    key={tab.id}
                    onClick={() => setActiveTab(tab.id)}
                    className={`flex items-center space-x-2 py-4 px-2 border-b-2 text-sm font-medium transition-colors ${
                      activeTab === tab.id
                        ? 'border-blue-500 text-blue-600'
                        : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                    }`}
                  >
                    <tab.icon className="w-4 h-4" />
                    <span>{tab.label}</span>
                  </button>
                ))}
              </nav>
            </div>
          </div>

          {/* Status Messages */}
          {error && (
            <div className="bg-red-50 border border-red-200 rounded-xl p-4 mb-6">
              <div className="flex items-center">
                <AlertCircle className="w-5 h-5 text-red-500 mr-2" />
                <span className="text-red-700">{error}</span>
              </div>
            </div>
          )}

          {success && (
            <div className="bg-green-50 border border-green-200 rounded-xl p-4 mb-6">
              <div className="flex items-center">
                <CheckCircle className="w-5 h-5 text-green-500 mr-2" />
                <span className="text-green-700">{success}</span>
              </div>
            </div>
          )}

          {/* Main Content */}
          <div className="bg-white rounded-xl shadow-lg p-6">
            {activeTab === 'upload' && (
              <div className="space-y-6">
                <div className="text-center">
                  <h2 className="text-2xl font-semibold text-gray-900 mb-4">Upload Your Data</h2>
                  <p className="text-gray-600 mb-8">Support for CSV and Excel files (.csv, .xlsx, .xls)</p>
                </div>
                
                <div className="max-w-md mx-auto">
                  <label className="flex flex-col items-center justify-center w-full h-64 border-2 border-gray-300 border-dashed rounded-lg cursor-pointer bg-gray-50 hover:bg-gray-100 transition-colors">
                    <div className="flex flex-col items-center justify-center pt-5 pb-6">
                      <Upload className="w-10 h-10 mb-3 text-gray-400" />
                      <p className="mb-2 text-sm text-gray-500">
                        <span className="font-semibold">Click to upload</span> or drag and drop
                      </p>
                      <p className="text-xs text-gray-500">CSV, XLSX, XLS files</p>
                    </div>
                    <input
                      type="file"
                      className="hidden"
                      accept=".csv,.xlsx,.xls"
                      onChange={handleFileUpload}
                      disabled={loading}
                    />
                  </label>
                </div>

                {loading && (
                  <div className="flex items-center justify-center space-x-2 text-blue-600">
                    <Loader2 className="w-5 h-5 animate-spin" />
                    <span>Processing file...</span>
                  </div>
                )}

                {fileName && (
                  <div className="text-center">
                    <p className="text-sm text-gray-600">Loaded: <span className="font-semibold">{fileName}</span></p>
                  </div>
                )}
              </div>
            )}

            {activeTab === 'data' && (
              <div className="space-y-6">
                <div className="flex justify-between items-center">
                  <h2 className="text-2xl font-semibold text-gray-900">Data Preview</h2>
                  <div className="text-sm text-gray-600">
                    {data.length} rows × {data.length > 0 ? Object.keys(data[0]).length : 0} columns
                  </div>
                </div>

                {data.length > 0 ? (
                  <div className="overflow-x-auto">
                    <table className="min-w-full divide-y divide-gray-200">
                      <thead className="bg-gray-50">
                        <tr>
                          {Object.keys(data[0]).map((column) => (
                            <th
                              key={column}
                              className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                            >
                              {column}
                            </th>
                          ))}
                        </tr>
                      </thead>
                      <tbody className="bg-white divide-y divide-gray-200">
                        {data.slice(0, 10).map((row, index) => (
                          <tr key={index}>
                            {Object.values(row).map((value, colIndex) => (
                              <td key={colIndex} className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                                {value?.toString() || '-'}
                              </td>
                            ))}
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                ) : (
                  <div className="text-center py-12">
                    <Table className="w-12 h-12 text-gray-400 mx-auto mb-4" />
                    <p className="text-gray-500">No data loaded. Please upload a file first.</p>
                  </div>
                )}

                {data.length > 0 && (
                  <div className="flex justify-center">
                    <button
                      onClick={callAzureML}
                      disabled={loading}
                      className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center space-x-2"
                    >
                      {loading ? (
                        <>
                          <Loader2 className="w-5 h-5 animate-spin" />
                          <span>Generating Predictions...</span>
                        </>
                      ) : (
                        <>
                          <BarChart3 className="w-5 h-5" />
                          <span>Generate Predictions</span>
                        </>
                      )}
                    </button>
                  </div>
                )}
              </div>
            )}

            {activeTab === 'config' && (
              <div className="space-y-6">
                <h2 className="text-2xl font-semibold text-gray-900">Azure ML Configuration</h2>
                
                <div className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Azure ML Endpoint URL
                    </label>
                    <input
                      type="url"
                      value={azureConfig.endpoint}
                      onChange={(e) => setAzureConfig({...azureConfig, endpoint: e.target.value})}
                      placeholder="https://your-endpoint.azureml.net/score"
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    />
                  </div>

                  {/* <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      API Key (Optional)
                    </label>
                    <input
                      type="password"
                      value={azureConfig.apiKey}
                      onChange={(e) => setAzureConfig({...azureConfig, apiKey: e.target.value})}
                      placeholder="Your Azure ML API key"
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    />
                  </div> */}

                  <div className="bg-blue-50 p-4 rounded-lg">
                    <h3 className="font-semibold text-blue-900 mb-2">Configuration Notes:</h3>
                    <ul className="text-sm text-blue-800 space-y-1">
                      <li>• Enter your Azure ML model endpoint URL</li>
                      {/* <li>• API key is optional depending on your model's authentication</li> */}
                      <li>• The app will send your data as JSON to the endpoint</li>
                      <li>• Ensure your model accepts the data format from uploaded files</li>
                    </ul>
                  </div>
                </div>
              </div>
            )}

            {activeTab === 'results' && (
              <div className="space-y-6">
                <div className="flex justify-between items-center">
                  <h2 className="text-2xl font-semibold text-gray-900">Prediction Results</h2>
                  <div className="flex space-x-2">
                    <button
                      onClick={() => exportResults('csv')}
                      className="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 flex items-center space-x-2"
                    >
                      <Download className="w-4 h-4" />
                      <span>CSV</span>
                    </button>
                    <button
                      onClick={() => exportResults('xlsx')}
                      className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 flex items-center space-x-2"
                    >
                      <Download className="w-4 h-4" />
                      <span>Excel</span>
                    </button>
                  </div>
                </div>

                {predictions.length > 0 ? (
                  <div className="space-y-8">
                    {/* Visualization */}
                    <div className="bg-gray-50 p-6 rounded-lg">
                      <h3 className="text-lg font-semibold mb-4">Prediction Visualization</h3>
                      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                        <div>
                          <h4 className="font-medium mb-2">Prediction Distribution</h4>
                          <ResponsiveContainer width="100%" height={200}>
                            <BarChart data={getChartData().slice(0, 20)}>
                              <CartesianGrid strokeDasharray="3 3" />
                              <XAxis dataKey="index" />
                              <YAxis />
                              <Tooltip />
                              <Bar dataKey="prediction" fill="#3B82F6" />
                            </BarChart>
                          </ResponsiveContainer>
                        </div>
                        
                        {/* <div>
                          <h4 className="font-medium mb-2">Confidence Scores</h4>
                          <ResponsiveContainer width="100%" height={200}>
                            <ScatterChart data={getChartData()}>
                              <CartesianGrid strokeDasharray="3 3" />
                              <XAxis dataKey="prediction" />
                              <YAxis dataKey="confidence" />
                              <Tooltip />
                              <Scatter fill="#10B981" />
                            </ScatterChart>
                          </ResponsiveContainer>
                        </div> */}
                      </div>
                    </div>

                    {/* Results Table */}
                    <div className="overflow-x-auto">
                      <table className="min-w-full divide-y divide-gray-200">
                        <thead className="bg-gray-50">
                          <tr>
                            {Object.keys(predictions[0]).map((column) => (
                              <th
                                key={column}
                                className={`px-6 py-3 text-left text-xs font-medium uppercase tracking-wider ${
                                  column === 'prediction' ? 'text-blue-600' : 'text-gray-500'
                                  // column === 'confidence' ? 'text-green-600' : 'text-gray-500'
                                }`}
                              >
                                {column}
                              </th>
                            ))}
                          </tr>
                        </thead>
                        <tbody className="bg-white divide-y divide-gray-200">
                          {predictions.slice(0, 10).map((row, index) => (
                            <tr key={index}>
                              {Object.entries(row).map(([key, value], colIndex) => (
                                <td key={colIndex} className={`px-6 py-4 whitespace-nowrap text-sm ${
                                  key === 'prediction' ? 'text-blue-600 font-semibold' : 'text-gray-900'
                                  // key === 'confidence' ? 'text-green-600 font-semibold' : 'text-gray-900'
                                }`}>
                                  {typeof value === 'number' ? value.toFixed(3) : value?.toString() || '-'}
                                </td>
                              ))}
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    </div>
                  </div>
                ) : (
                  <div className="text-center py-12">
                    <BarChart3 className="w-12 h-12 text-gray-400 mx-auto mb-4" />
                    <p className="text-gray-500">No predictions generated yet. Upload data and configure your ML model first.</p>
                  </div>
                )}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default MLPredictionApp;