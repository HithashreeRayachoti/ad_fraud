# Ad Fraud Detection System

A comprehensive real-time ad fraud detection system that uses machine learning to identify fraudulent clicks and bot traffic on advertising landing pages.

## Project Overview

This system provides real-time detection of fraudulent ad clicks by analyzing user behavior patterns including mouse movements, click patterns, and interaction timing. The solution combines client-side tracking, machine learning classification, and real-time dashboard visualization with sub-second response times for production environments.

## System Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend       │    │  ML Pipeline    │
│   (React)       │◄──►│   (Flask)       │◄──►│  (Scikit-learn) │
│                 │    │                 │    │                 │
│ • User Tracking │    │ • API Endpoints │    │ • Model Training│
│ • Data Collection│    │ • Real-time ML  │    │ • Feature Eng.  │
│ • Dashboard     │    │ • Data Logging  │    │ • Evaluation    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Technical Components

**Client-Side Tracking Layer**
- Event-driven JavaScript listeners for DOM interactions
- Crypto API for secure session ID generation
- Real-time data serialization and transmission
- Asynchronous HTTP requests with keepalive functionality

**Server-Side Processing Layer**
- Flask WSGI application with CORS middleware
- NumPy-based vectorized feature engineering
- Joblib model deserialization and prediction pipeline
- JSON-based persistent storage with atomic file operations

**Machine Learning Pipeline**
- Ensemble learning with Random Forest, XGBoost, and Gradient Boosting
- Feature extraction from temporal and spatial behavioral data
- Cross-validation with stratified sampling for imbalanced datasets
- Model persistence and versioning with Joblib serialization

## Features and Capabilities

### Real-time Detection Engine
- **Mouse Movement Tracking**: Captures coordinate paths with millisecond precision timing
- **Click Pattern Analysis**: Monitors click frequency, velocity, and spatial distribution
- **Behavioral Profiling**: Analyzes session duration, interaction velocity, and movement entropy
- **Instant Classification**: Sub-100ms prediction latency for real-time bot detection

### Machine Learning Models
- **Random Forest Classifier**: Ensemble method with 100 decision trees for robust predictions
- **XGBoost Classifier**: Gradient boosting with optimized hyperparameters for imbalanced data
- **Gradient Boosting**: Scikit-learn implementation with configurable learning rate and tree depth

### Analytics Dashboard
- **Traffic Source Visualization**: Interactive pie charts with React-based state management
- **Temporal Analysis**: Time-series line charts with configurable time windows
- **Session Logs**: Real-time log streaming with pagination and filtering
- **Performance Metrics**: Live accuracy, precision, recall, and F1-score monitoring

## Project Structure

```
c:\ad_fraud\
├── ad_fraud/                    # Frontend React application
│   ├── src/
│   │   ├── App.js              # Main application component with React Router
│   │   ├── clickceaseTracker.js # Client-side tracking implementation
│   │   └── dashboard.js        # Analytics dashboard component
│   ├── public/
│   │   └── kpmg-logo-1.png     # Static assets
│   └── package.json            # Node.js dependencies
├── server/                      # Backend Flask API
│   ├── app.py                  # Main server application with ML integration
│   └── click_logs.json         # Session data storage
├── MachineLearning/            # ML pipeline and models
│   ├── train_model.py          # Model training with hyperparameter tuning
│   ├── test_model.py           # Model evaluation and performance metrics
│   ├── scripts.py              # Data preprocessing and feature engineering
│   ├── savedModels/            # Serialized model artifacts
│   │   ├── random_forest_classifier.joblib
│   │   ├── xgboost_classifier.joblib
│   │   └── gradient_boosting_classifier.joblib
│   └── ProcessedPhase1/        # Processed training datasets
│       ├── train_features.csv
│       ├── train_labels.csv
│       └── test_features.csv
├── dashboard/                   # Standalone dashboard application
│   └── src/App.js              # Dashboard React component with Recharts
├── python_bot/                 # Bot simulation for testing
│   └── bot.py                  # Selenium WebDriver automation
└── README.md                   # Technical documentation
```

## Technology Stack

### Frontend Technologies
- **React.js 18.x**: Component-based UI framework with hooks and context API
- **React Router 6.x**: Client-side routing with browser history management
- **Recharts 2.x**: SVG-based charting library built on D3.js
- **JavaScript ES6+**: Modern ECMAScript features including async/await and modules
- **CSS3**: Flexbox and Grid layouts with responsive design patterns

### Backend Technologies
- **Flask 2.x**: Lightweight WSGI web framework with blueprint architecture
- **Flask-CORS**: Cross-Origin Resource Sharing middleware for API access
- **NumPy 1.24+**: Vectorized numerical computing for feature calculations
- **Pandas 2.x**: DataFrame operations for data manipulation and analysis
- **Python 3.8+**: Type hints, dataclasses, and asyncio support

### Machine Learning Stack
- **Scikit-learn 1.3+**: ML algorithms including Random Forest and Gradient Boosting
- **XGBoost 1.7+**: Optimized gradient boosting framework with GPU acceleration
- **Joblib 1.3+**: Efficient serialization for NumPy arrays and ML models
- **Matplotlib 3.x**: Publication-quality plotting with backend configuration
- **Seaborn 0.12+**: Statistical data visualization with improved aesthetics

### Development and Testing
- **Selenium WebDriver 4.x**: Browser automation for bot simulation
- **ChromeDriver**: Headless browser testing with DevTools Protocol
- **Node.js 18+**: JavaScript runtime with npm package management
- **Python Virtual Environments**: Isolated dependency management

## System Requirements

### Minimum Hardware Specifications
- **CPU**: Dual-core processor (2.0 GHz or higher)
- **RAM**: 4 GB minimum, 8 GB recommended for ML training
- **Storage**: 2 GB available disk space for models and datasets
- **Network**: Broadband internet connection for external dependencies

### Software Prerequisites
- **Node.js**: Version 14.0 or higher with npm 6.0+
- **Python**: Version 3.8 or higher with pip 20.0+
- **Chrome Browser**: Version 90 or higher for Selenium automation
- **Git**: Version 2.0 or higher for source control

## Installation and Configuration

### 1. Repository Setup
```bash
git clone <repository-url>
cd ad_fraud
```

### 2. Backend Environment Setup
```bash
cd server
pip install -r requirements.txt
# Or install manually:
pip install flask==2.3.3 flask-cors==4.0.0 pandas==2.0.3 numpy==1.24.3 
pip install scikit-learn==1.3.0 xgboost==1.7.6 joblib==1.3.2
pip install matplotlib==3.7.2 seaborn==0.12.2
python app.py
```

### 3. Frontend Environment Setup
```bash
cd ad_fraud
npm install --production
npm audit fix
npm start
```

### 4. Dashboard Environment Setup
```bash
cd dashboard
npm install react@18.2.0 react-dom@18.2.0 recharts@2.8.0
npm start
```

### 5. Machine Learning Pipeline Setup
```bash
cd MachineLearning
# Ensure data preprocessing is complete
python scripts.py
# Train all three models with cross-validation
python train_model.py
# Evaluate model performance on test set
python test_model.py
```

## System Operation

### Service Startup Sequence
1. **Backend API Server**: `python server/app.py` (Binds to localhost:5000)
2. **Frontend Application**: `npm start` in `ad_fraud/` (Serves on localhost:3000)
3. **Analytics Dashboard**: `npm start` in `dashboard/` (Available on localhost:3001)

### Real-time Monitoring
1. **Landing Page**: Navigate to `http://localhost:3000` for user interaction tracking
2. **Analytics Interface**: Access `http://localhost:3000/dashboard` for real-time metrics
3. **Server Logs**: Monitor console output for classification results and API requests

### Bot Simulation Testing
```bash
cd python_bot
pip install selenium==4.15.0 webdriver-manager==4.0.1
python bot.py
```

## Machine Learning Implementation

### Feature Engineering Pipeline

The system implements a comprehensive feature extraction pipeline that processes raw user interaction data into ML-ready features:

```python
def create_feature_vector(session_data: dict):
    # Temporal features
    session_duration = calculate_session_duration(timestamps)
    
    # Spatial features  
    mouse_distance = calculate_euclidean_distance(coordinates)
    avg_velocity = mouse_distance / (session_duration / 1000.0)
    
    # Behavioral features
    click_frequency = count_click_events(actions)
    movement_entropy = calculate_movement_entropy(coordinates)
    
    return feature_vector
```

### Feature Set Specification

| Feature Name | Data Type | Description | Units | Range |
|--------------|-----------|-------------|-------|-------|
| `total_events` | Integer | Count of all user interactions | Events | 0-∞ |
| `mouse_distance` | Float | Cumulative pixel distance traveled | Pixels | 0.0-∞ |
| `session_duration_ms` | Integer | Total session time | Milliseconds | 0-∞ |
| `avg_velocity` | Float | Average mouse movement speed | Pixels/second | 0.0-∞ |
| `click_count` | Integer | Number of click events recorded | Clicks | 0-∞ |

### Model Architecture and Hyperparameters

**Random Forest Classifier**
```python
RandomForestClassifier(
    n_estimators=100,
    max_depth=None,
    min_samples_split=2,
    min_samples_leaf=1,
    random_state=42,
    n_jobs=-1
)
```

**XGBoost Classifier**
```python
XGBClassifier(
    n_estimators=100,
    learning_rate=0.1,
    max_depth=6,
    subsample=0.8,
    colsample_bytree=0.8,
    random_state=42,
    use_label_encoder=False,
    eval_metric='mlogloss'
)
```

**Gradient Boosting Classifier**
```python
GradientBoostingClassifier(
    n_estimators=100,
    learning_rate=0.1,
    max_depth=3,
    subsample=1.0,
    random_state=42
)
```

### Model Performance Evaluation

The system implements comprehensive evaluation metrics:

- **Accuracy Score**: Overall classification accuracy across all classes
- **Precision**: True positives divided by (true positives + false positives)
- **Recall**: True positives divided by (true positives + false negatives)
- **F1-Score**: Harmonic mean of precision and recall
- **ROC AUC**: Area under the Receiver Operating Characteristic curve
- **Confusion Matrix**: Detailed breakdown of classification results

### Real-time Classification Pipeline

```python
# Feature extraction from live session data
features = create_feature_vector(session_data)
feature_matrix = pd.DataFrame([features])[MODEL_FEATURES]

# Model prediction with confidence scoring
prediction_proba = model.predict_proba(feature_matrix)
prediction_class = model.predict(feature_matrix)

# Classification mapping
classification = LABEL_MAPPING.get(prediction_class[0], 'Unknown')
confidence_score = np.max(prediction_proba)
```

## API Documentation

### POST /log-visit

Accepts user session data and returns real-time fraud classification.

**Request Headers:**
```
Content-Type: application/json
User-Agent: <browser-user-agent>
```

**Request Payload:**
```json
{
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "total_behaviour": ["m(150,200)", "m(151,201)", "c(l)", "m(160,210)"],
  "mousemove_times": [1000, 1050, 1100, 1150],
  "mousemove_total_behaviour": [
    {"x": 150, "y": 200},
    {"x": 151, "y": 201},
    {"x": 160, "y": 210}
  ],
  "Mousemove_visited_urls": 3
}
```

**Response:**
```json
{
  "status": "ok",
  "prediction": "Human",
  "confidence": 0.87,
  "processing_time_ms": 45
}
```

**Status Codes:**
- `200 OK`: Successful classification
- `400 Bad Request`: Invalid request payload
- `500 Internal Server Error`: Model prediction failure

### GET /api/sessions

Retrieves paginated session logs for dashboard visualization.

**Query Parameters:**
- `limit`: Maximum number of sessions to return (default: 100)
- `offset`: Number of sessions to skip (default: 0)
- `filter`: Filter by prediction type ('Human', 'Bot', or 'All')

**Response:**
```json
{
  "sessions": [
    {
      "session_id": "550e8400-e29b-41d4-a716-446655440000",
      "timestamp": "2024-01-15T14:30:45.123Z",
      "prediction": "Bot",
      "confidence": 0.92,
      "ip_address": "192.168.1.100",
      "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
  ],
  "total_count": 1587,
  "page_info": {
    "has_next": true,
    "has_previous": false
  }
}
```

## Configuration Management

### Model Selection Configuration

Edit the `MODEL_PATH` variable in `server/app.py` to switch between trained models:

```python
# Production model configuration
MODEL_PATH = os.path.join('..', 'MachineLearning', 'savedModels', 'xgboost_classifier.joblib')

# Alternative model options:
# MODEL_PATH = 'savedModels/random_forest_classifier.joblib'
# MODEL_PATH = 'savedModels/gradient_boosting_classifier.joblib'
```

### Feature Set Customization

Modify the `MODEL_FEATURES` list to adjust the feature set used for predictions:

```python
MODEL_FEATURES = [
    'total_events',
    'mouse_distance', 
    'session_duration_ms',
    'avg_velocity',
    'click_count'
]

# Extended feature set (requires model retraining):
# MODEL_FEATURES.extend(['movement_entropy', 'click_variance', 'pause_frequency'])
```

### Logging Configuration

Configure logging levels and output destinations:

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('fraud_detection.log'),
        logging.StreamHandler()
    ]
)
```

## Testing and Validation

### Unit Testing Framework

```bash
# Install testing dependencies
pip install pytest==7.4.0 pytest-cov==4.1.0

# Run unit tests with coverage
pytest tests/ --cov=server --cov-report=html
```

### Integration Testing

```bash
# Test API endpoints
python -m pytest tests/test_api.py -v

# Test ML pipeline
python -m pytest tests/test_ml_pipeline.py -v
```

### Performance Testing

```bash
# Load testing with Apache Bench
ab -n 1000 -c 10 http://localhost:5000/log-visit

# Memory profiling
python -m memory_profiler server/app.py
```

### Model Validation

```bash
cd MachineLearning
# Cross-validation with stratified k-fold
python test_model.py --cross-validate --folds=5

# Feature importance analysis
python test_model.py --feature-importance
```

## Performance Metrics and Monitoring

### System Performance Indicators

- **Prediction Latency**: Target <100ms per classification
- **Memory Usage**: <512MB baseline, <2GB during training
- **CPU Utilization**: <20% during normal operation
- **Disk I/O**: <10MB/hour for logging operations

### Model Performance Metrics

```python
# Classification metrics
accuracy = accuracy_score(y_true, y_pred)
precision = precision_score(y_true, y_pred, average='weighted')
recall = recall_score(y_true, y_pred, average='weighted')
f1 = f1_score(y_true, y_pred, average='weighted')

# ROC analysis
fpr, tpr, thresholds = roc_curve(y_true, y_proba)
auc_score = auc(fpr, tpr)
```

### Real-time Monitoring

```python
# Performance monitoring middleware
@app.before_request
def before_request():
    g.start_time = time.time()

@app.after_request  
def after_request(response):
    response_time = time.time() - g.start_time
    logger.info(f"Request processed in {response_time:.3f}s")
    return response
```

## Security Considerations

### Data Privacy and Protection
- **Local Data Storage**: Session data stored locally in JSON format
- **No External Transmission**: Behavioral data never leaves the local environment
- **Session Anonymization**: UUIDs used instead of personally identifiable information
- **Data Retention Policies**: Configurable log rotation and archival

### Model Security
- **Server-Side Models**: ML models stored on backend to prevent tampering
- **Input Validation**: Comprehensive sanitization of incoming session data
- **Rate Limiting**: Configurable request rate limiting for DoS protection
- **Authentication**: Optional API key authentication for production deployments

### Production Security Hardening

```python
# Security headers middleware
@app.after_request
def security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    return response

# Input validation
from marshmallow import Schema, fields, validate

class SessionSchema(Schema):
    session_id = fields.UUID(required=True)
    total_behaviour = fields.List(fields.String(), required=True)
    mousemove_times = fields.List(fields.Integer(), required=True)
```


