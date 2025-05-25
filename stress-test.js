import http from 'k6/http';
import { sleep, check } from 'k6';
import { Rate } from 'k6/metrics';

// Custom metric for error rate
const errorRate = new Rate('errors');

// Test configuration
export const options = {
  stages: [ 
    { duration: '1m', target: 20 },  // Ramp up to 20 users
    { duration: '3m', target: 20 },  // Stay at 20 users
    { duration: '1m', target: 50 },  // Ramp up to 50 users
    { duration: '3m', target: 50 },  // Stay at 50 users
    { duration: '1m', target: 0 },   // Ramp down to 0 users
  ],
  thresholds: {
    http_req_duration: ['p(95)<2000'], // 95% of requests should be below 2s
    errors: ['rate<0.1'],              // Error rate should be below 10%
  },
};

// JWT token - Replace with your actual token
const JWT_TOKEN = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJPbmxpbmUgSldUIEJ1aWxkZXIiLCJpYXQiOjE3NDMzNTQ4NzcsImV4cCI6MTc3NDg5MDg5MiwiYXVkIjoid3d3LmV4YW1wbGUuY29tIiwic3ViIjoianJvY2tldEBleGFtcGxlLmNvbSIsIkdpdmVuTmFtZSI6IkpvaG5ueSIsIlN1cm5hbWUiOiJSb2NrZXQiLCJFbWFpbCI6Impyb2NrZXRAZXhhbXBsZS5jb20iLCJSb2xlIjpbIk1hbmFnZXIiLCJQcm9qZWN0IEFkbWluaXN0cmF0b3IiXX0.eKKappNb0N-vJtrOnoOau-AnXvEN07Up_HspTt5pia8';

// Test function
export default function () {
  const BASE_URL = 'http://lb-entrega4-app-55551883.us-east-1.elb.amazonaws.com'; // Updated to use Docker host
  const headers = {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${JWT_TOKEN}`
  };

  const randomPart = Math.floor(Math.random() * 1e9); // Random number for uniqueness
  const postPayload = JSON.stringify({
    email: `test${__VU}_${__ITER}_${randomPart}@example.com`, // Unique email per request
    app_uuid: 'b7e1c7e2-2c3a-4e7a-9e2a-8b1e2f3c4d5f',
    blocked_reason: 'Test blacklist'
  });

  const postResponse = http.post(`${BASE_URL}/blacklists`, postPayload, {
    headers: headers
  });

  check(postResponse, {
    'POST blacklist status is 201': (r) => r.status === 201,
  }) || errorRate.add(1);

  sleep(1);

  // Test GET request to check blacklist status
  const getResponse = http.get(`${BASE_URL}/blacklists/test${__VU}@example.com`, {
    headers: headers
  });
  
  check(getResponse, {
    'GET blacklist status is 200': (r) => r.status === 200,
  }) || errorRate.add(1);

  sleep(1);
} 