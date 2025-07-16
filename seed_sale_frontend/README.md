# Seed Sale Prediction - React Frontend

A modern, responsive React application for uploading data files and getting ML predictions through a REST API. Built with React, Tailwind CSS, and powerful data visualization libraries.

## Features

- 📁 **File Upload**: Drag-and-drop support for CSV and Excel files (.csv, .xlsx, .xls)
- 📊 **Data Preview**: Interactive table showing uploaded data with column information
- ⚙️ **ML Configuration**: Easy setup for Azure ML or local Flask API endpoints
- 🔮 **Predictions**: Real-time ML predictions with confidence scores
- 📈 **Visualizations**: Interactive charts showing prediction distributions and confidence
- 📤 **Export**: Download results as CSV or Excel files
- 🎨 **Modern UI**: Clean, responsive design with Tailwind CSS

## Tech Stack

- **React 18** - Modern React with hooks
- **Tailwind CSS** - Utility-first CSS framework
- **Recharts** - Beautiful, customizable charts
- **SheetJS (xlsx)** - Excel file processing
- **Papaparse** - Robust CSV parsing
- **Lucide React** - Beautiful icons

## Quick Start

### Prerequisites

- Node.js 16+ 
- npm or yarn

### Installation

1. **Clone or create the project:**
   ```bash
   npx create-react-app seed_sale_prediction
   cd seed_sale_prediction
   ```

2. **Install dependencies:**
   ```bash
   npm install xlsx papaparse recharts lucide-react
   ```

3. **Install and configure Tailwind CSS:**
   ```bash
   npm install -D tailwindcss postcss autoprefixer
   npx tailwindcss init -p
   ```

4. **Configure Tailwind** - Update `tailwind.config.js`:
   ```javascript
   module.exports = {
     content: [
       "./src/**/*.{js,jsx,ts,tsx}",
     ],
     theme: {
       extend: {},
     },
     plugins: [],
   }
   ```

5. **Add Tailwind directives** to `src/index.css`:
   ```css
   @tailwind base;
   @tailwind components;
   @tailwind utilities;
   ```

6. **Replace `src/App.js`** with the ML Prediction Dashboard component

7. **Start the development server:**
   ```bash
   npm start
   ```

The app will be available at `http://localhost:3000`

## Usage

### 1. Upload Data
- Click the upload area or drag & drop your CSV/Excel file
- Supported formats: `.csv`, `.xlsx`, `.xls`
- The app will automatically parse and display your data

### 2. Configure ML Endpoint
- Navigate to the "ML Config" tab
- Enter your API endpoint URL (e.g., `http://localhost:5000/predict`)
- Add API key if required (optional for local testing)

### 3. Generate Predictions
- Review your data in the "Data Preview" tab
- Click "Generate Predictions" to call your ML model
- View results with confidence scores

### 4. Analyze Results
- Interactive charts showing prediction distributions
- Sortable table with original data + predictions
- Export results as CSV or Excel

## Configuration

### Local Flask API
```javascript
// For local testing with Flask API
Endpoint: http://localhost:5000/predict
API Key: (leave empty)
```

### Azure ML
```javascript
// For Azure ML deployment
Endpoint: https://your-endpoint.azureml.net/score
API Key: your-azure-ml-api-key
```

## File Structure

```
src/
├── App.js              # Main ML Prediction Dashboard component
├── index.css           # Tailwind CSS imports
├── index.js            # React entry point
└── ...
```

## Data Format

The app expects your data to have:
- **Headers**: First row should contain column names
- **Mixed data types**: Supports both numerical and categorical columns
- **Clean data**: Missing values will be handled automatically

Example CSV structure:
```csv
PRODUCT,SALESYEAR,LIFECYCLE,STATE,RELEASE_YEAR,DISEASE_RESISTANCE,INSECT_RESISTANCE,PROTECTION,DROUGHT_TOLERANCE,BRITTLE_STALK,PLANT_HEIGHT,RELATIVE_MATURITY,UNITS
P140,2021,ESTABLISHED,Texas,2016,0,0,1,4.0,3.0,2.0,4,3.5
P145,2021,INTRODUCTION,Texas,2020,0,1,1,2.0,2.0,1.0,3,0.7
```

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -m 'Add feature'`
4. Push to branch: `git push origin feature-name`
5. Submit a pull request

## License

MIT License - feel free to use this project