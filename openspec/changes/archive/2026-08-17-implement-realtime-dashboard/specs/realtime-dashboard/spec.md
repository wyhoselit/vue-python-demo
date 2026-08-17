## ADDED Requirements

### Requirement: Real-time API Request Trend Visualization
The dashboard SHALL display a real-time area chart showing the trend of API requests over time.

#### Scenario: Chart updates with new data points
- **WHEN** new real-time data is received every 5 seconds
- **THEN** the API Request Trend chart SHALL update to include the latest data point and maintain a window of the last 20 data points.

### Requirement: Average API Response Time Trend Visualization
The dashboard SHALL display a real-time line chart showing the average response time of API requests over time.

#### Scenario: Chart updates with new data points
- **WHEN** new real-time data is received every 5 seconds
- **THEN** the Average API Response Time chart SHALL update to include the latest data point and maintain a window of the last 20 data points.

### Requirement: API Status Code Distribution
The dashboard SHALL display a real-time donut chart showing the distribution of API response status codes (2xx, 4xx, 5xx).

#### Scenario: Chart updates with latest distribution
- **WHEN** new real-time data is received every 5 seconds
- **THEN** the API Status Code Distribution chart SHALL update to reflect the status code counts of the latest data point.

### Requirement: Active Users Trend Visualization
The dashboard SHALL display a real-time bar chart showing the trend of active users over time.

#### Scenario: Chart updates with new data points
- **WHEN** new real-time data is received every 5 seconds
- **THEN** the Active Users Trend chart SHALL update to include the latest data point and maintain a window of the last 20 data points.
