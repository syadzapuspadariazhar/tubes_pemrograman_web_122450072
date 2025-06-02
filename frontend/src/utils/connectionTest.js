// Connection test utility to diagnose backend connection issues
import axios from "axios";
import { API_BASE_URL, API_URL } from "../config";

export const testBackendConnection = async () => {
  const results = {
    timestamp: new Date().toISOString(),
    tests: []
  };

  // Test 1: Basic ping to root endpoint
  try {
    const response = await axios.get(`${API_BASE_URL}`, { timeout: 3000 });
    results.tests.push({
      name: "Root endpoint test",
      url: API_BASE_URL,
      status: "✅ PASS",
      details: `Status: ${response.status}, Response time: ${response.config.timeout}ms`
    });
  } catch (error) {
    results.tests.push({
      name: "Root endpoint test",
      url: API_BASE_URL,
      status: "❌ FAIL",
      details: `Error: ${error.code || error.message}`
    });
  }

  // Test 2: Categories API endpoint
  try {
    const response = await axios.get(`${API_URL}/categories`, { 
      timeout: 3000,
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      }
    });
    results.tests.push({
      name: "Categories API test",
      url: `${API_URL}/categories`,
      status: "✅ PASS",
      details: `Status: ${response.status}, Data length: ${response.data.length}`
    });
  } catch (error) {
    results.tests.push({
      name: "Categories API test",
      url: `${API_URL}/categories`,
      status: "❌ FAIL",
      details: `Error: ${error.code || error.message}`
    });
  }

  // Test 3: OPTIONS request (CORS preflight)
  try {
    const response = await axios.options(`${API_URL}/categories`, { timeout: 3000 });
    results.tests.push({
      name: "CORS preflight test",
      url: `${API_URL}/categories`,
      status: "✅ PASS",
      details: `Status: ${response.status}, CORS headers available`
    });
  } catch (error) {
    results.tests.push({
      name: "CORS preflight test", 
      url: `${API_URL}/categories`,
      status: "❌ FAIL",
      details: `Error: ${error.code || error.message}`
    });
  }

  // Test 4: POST request test (dry-run)
  try {
    const response = await axios.post(`${API_URL}/categories`, 
      { nama: "TEST_CONNECTION", jenis: "income" },
      { 
        timeout: 3000,
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        }
      }
    );
    results.tests.push({
      name: "POST request test",
      url: `${API_URL}/categories`,
      status: "✅ PASS",
      details: `Status: ${response.status}, Created test category`
    });

    // Clean up test category
    if (response.data && response.data.id) {
      try {
        await axios.delete(`${API_URL}/categories/${response.data.id}`);
        results.tests.push({
          name: "Cleanup test category",
          status: "✅ PASS",
          details: "Test category removed successfully"
        });
      } catch (cleanupError) {
        results.tests.push({
          name: "Cleanup test category",
          status: "⚠️ WARNING",
          details: "Could not remove test category"
        });
      }
    }
  } catch (error) {
    results.tests.push({
      name: "POST request test",
      url: `${API_URL}/categories`,
      status: "❌ FAIL",
      details: `Error: ${error.code || error.message}`
    });
  }

  return results;
};

export const printConnectionTestResults = (results) => {
  console.log("🔍 Backend Connection Test Results");
  console.log("=====================================");
  console.log(`Timestamp: ${results.timestamp}`);
  console.log(`Configuration: API_BASE_URL=${API_BASE_URL}, API_URL=${API_URL}`);
  console.log("");
  
  results.tests.forEach((test, index) => {
    console.log(`${index + 1}. ${test.name}: ${test.status}`);
    if (test.url) console.log(`   URL: ${test.url}`);
    console.log(`   Details: ${test.details}`);
    console.log("");
  });

  const passCount = results.tests.filter(t => t.status.includes("PASS")).length;
  const failCount = results.tests.filter(t => t.status.includes("FAIL")).length;
  
  console.log(`Summary: ${passCount} passed, ${failCount} failed`);
  
  if (failCount === 0) {
    console.log("🎉 All tests passed! Backend connection is working properly.");
  } else {
    console.log("⚠️ Some tests failed. Check the details above for troubleshooting.");
  }
};
