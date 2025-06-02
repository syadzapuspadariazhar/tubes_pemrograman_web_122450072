const fs = require('fs');
const http = require('http');
const { exec } = require('child_process');
const path = require('path');

console.log('Memeriksa server backend sebelum memulai frontend...');

// Path to start_backend.bat relative to frontend folder
const startBackendScript = path.join('..', 'start_backend.bat');

// Function to check if the backend is running
function checkBackendServer(url) {
  return new Promise((resolve) => {    http.get(url, (res) => {
      if (res.statusCode === 200) {
        console.log('✅ Server backend sedang berjalan!');
        resolve(true);
      } else {
        console.log(`❌ Server backend mengembalikan status: ${res.statusCode}`);
        resolve(false);
      }
    }).on('error', () => {
      console.log('❌ Server backend tidak berjalan');
      resolve(false);
    });
  });
}

// Function to start the backend server
function startBackendServer() {
  return new Promise((resolve) => {    console.log('Memulai server backend...');
    
    // Check if start_backend.bat exists
    if (!fs.existsSync(startBackendScript)) {
      console.log(`❌ Script starter backend tidak ditemukan di: ${startBackendScript}`);
      resolve(false);
      return;
    }
    
    // Execute the start_backend.bat in a new window
    const process = exec(`start cmd.exe /K "${startBackendScript}"`, (error) => {
      if (error) {
        console.log('❌ Gagal memulai server backend:', error);
        resolve(false);
        return;
      }
    });
    
    console.log('⏳ Menunggu server backend dimulai...');
    // Give some time for the server to start
    setTimeout(() => resolve(true), 3000);
  });
}

async function main() {
  try {
    // Check if backend is already running
    const isRunning = await checkBackendServer('http://localhost:6543/api/categories');
    
    if (!isRunning) {
      // Ask user if they want to start the backend
      const readline = require('readline').createInterface({
        input: process.stdin,
        output: process.stdout
      });
        readline.question('Server backend tidak berjalan. Apakah Anda ingin menjalankannya? (y/n) ', async (answer) => {
        readline.close();
        
        if (answer.toLowerCase() === 'y') {
          await startBackendServer();
          console.log('Memulai frontend...');
        } else {
          console.log('⚠️ Peringatan: Frontend akan dimulai tanpa backend. Permintaan API akan gagal.');
          console.log('Anda dapat menjalankan server backend secara manual dengan menjalankan start-app.bat');
          console.log('Atau jalankan start_backend.bat pada terminal terpisah.');
        }
      });
    } else {
      console.log('Starting frontend...');
    }
  } catch (error) {
    console.error('Error checking backend server:', error);
    console.log('Starting frontend anyway...');
  }
}

main();
