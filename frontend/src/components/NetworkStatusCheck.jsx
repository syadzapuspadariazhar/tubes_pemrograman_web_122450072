import { useState, useEffect } from "react";
import axios from "axios";
import { API_BASE_URL } from "../config";

export default function NetworkStatusCheck({ apiUrl = API_BASE_URL }) {
  const [status, setStatus] = useState("checking"); // "online", "offline", "checking"
  const [errorMessage, setErrorMessage] = useState("");
  const [checkCount, setCheckCount] = useState(0);
  const [showDetails, setShowDetails] = useState(false);  useEffect(() => {
    // Function to check backend availability
    const checkBackend = async () => {
      try {
        const startTime = Date.now();
        
        // Try the categories endpoint with a shorter timeout
        await axios.get(`${apiUrl}/api/categories`, { 
          timeout: 5000,
          params: { _t: new Date().getTime() }, // Cache-busting
          headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
          }
        });
        
        const responseTime = Date.now() - startTime;
        setStatus("online");
        setErrorMessage(`Response time: ${responseTime}ms`);
        
        // Reset consecutive failures if successful
        window.backendConsecutiveFailures = 0;
        
        // Update page title if needed
        if (document.title.includes("(Offline)")) {
          document.title = document.title.replace(" (Offline)", "");
        }
        
      } catch (error) {
        // Track consecutive failures
        window.backendConsecutiveFailures = (window.backendConsecutiveFailures || 0) + 1;
        const failureCount = window.backendConsecutiveFailures;
        
        setStatus("offline");
        
        // Update page title to show offline status
        if (!document.title.includes("(Offline)")) {
          document.title = `${document.title} (Offline)`;
        }
        
        if (error.response) {
          // Server responded with error status
          setErrorMessage(`Error server: ${error.response.status} ${error.response.statusText}`);
        } else if (error.request) {
          // No response received
          setErrorMessage(`Tidak ada respons dari server ${apiUrl}. Periksa apakah backend berjalan. (${failureCount} kali gagal berturut-turut)`);
          
          // Try to ping different endpoints with increasing timeout for reliability
          const checkEndpoints = async () => {
            try {
              // Try root endpoint first
              await axios.get(`${apiUrl}`, { timeout: 5000 });
              setStatus("online");
              setErrorMessage("Koneksi tersedia tetapi API tidak merespon");
              return true;
            } catch (e1) {
              try {
                // Then try OPTIONS request which might be allowed by CORS
                await axios.options(`${apiUrl}/api/categories`, { timeout: 8000 });
                setStatus("online");
                setErrorMessage("Koneksi tersedia tetapi mungkin ada masalah CORS");
                return true;
              } catch (e2) {
                // All attempts failed
                return false;
              }
            }
          };
          
          // Only do additional checks after a few failures
          if (failureCount === 2) {
            setTimeout(() => {
              checkEndpoints();
            }, 2000);
          }
        } else {
          // Request setup error
          setErrorMessage(`Error permintaan: ${error.message}`);
        }
      } finally {
        setCheckCount((prev) => prev + 1);
      }
    };

    // Initial check
    checkBackend();

    // Set up periodic checks
    const intervalId = setInterval(checkBackend, 15000); // Check every 15 seconds

    return () => clearInterval(intervalId);
  }, [apiUrl]);

  // Don't show on first check or when online (after 2 checks)
  if ((status === "online" && checkCount > 1) || checkCount === 0) {
    return null;
  }

  return (
    <div className={`fixed bottom-4 right-4 p-3 rounded-md shadow-md transition-all ${
      status === "checking" ? "bg-blue-100 text-blue-800" :
      status === "offline" ? "bg-red-100 text-red-800" :
      "bg-green-100 text-green-800"
    }`}>
      <div className="flex items-center space-x-2">
        {status === "checking" && (
          <div className="h-5 w-5 rounded-full border-2 border-blue-600 border-t-transparent animate-spin"></div>
        )}
        {status === "offline" && (
          <svg
            xmlns="http://www.w3.org/2000/svg"
            className="h-5 w-5 text-red-600"
            viewBox="0 0 20 20"
            fill="currentColor"
          >
            <path
              fillRule="evenodd"
              d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
              clipRule="evenodd"
            />
          </svg>
        )}
        <div>          <div className="font-medium">
            {status === "checking" && "Memeriksa koneksi backend..."}
            {status === "offline" && `Backend di ${apiUrl} tidak tersambung!`}
          </div>
          <div className="text-sm">
            {status === "offline" && (
              <button 
                className="underline focus:outline-none" 
                onClick={() => setShowDetails(!showDetails)}
              >
                {showDetails ? "Sembunyikan detail" : "Tampilkan detail"}
              </button>
            )}
          </div>          {showDetails && (
            <div className="mt-2 text-sm">
              <div>Server: {apiUrl}</div>
              <div>Error: {errorMessage}</div>
              <div className="mt-2 text-xs">
                <ol className="list-decimal list-inside">
                  <li>Pastikan server backend berjalan</li>
                  <li>Periksa koneksi database PostgreSQL</li>
                  <li>Jalankan diagnose-backend.ps1 untuk diagnosis</li>
                </ol>
              </div>
              <button 
                onClick={() => {
                  window.location.reload();
                }}
                className="mt-2 bg-red-600 hover:bg-red-700 text-white px-3 py-1 rounded text-xs"
              >
                Refresh Aplikasi
              </button>
              <button 
                onClick={() => {
                  window.open(`${API_BASE_URL}/api/categories`, '_blank');
                }}
                className="ml-2 mt-2 bg-gray-600 hover:bg-gray-700 text-white px-3 py-1 rounded text-xs"
              >
                Tes API
              </button>
              <button
                onClick={() => {
                  // Try to guide user to start backend 
                  if (window.confirm('Apakah Anda ingin menjalankan server backend?')) {
                    alert('Jalankan file "start-app.bat" dan pilih opsi "Start Backend Only"\nLalu refresh halaman ini setelah server berjalan.');
                    
                    // Prepare a refresh after a short delay
                    setTimeout(() => {
                      if (window.confirm('Refresh halaman sekarang?')) {
                        window.location.reload();
                      }
                    }, 5000);
                  }
                }}
                className="ml-2 mt-2 bg-green-600 hover:bg-green-700 text-white px-3 py-1 rounded text-xs"
              >
                Jalankan Backend
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
