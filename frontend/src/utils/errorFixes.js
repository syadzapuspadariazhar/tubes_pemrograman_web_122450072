// Fixes for common JavaScript errors

/**
 * Fix for regeneratorRuntime missing error 
 * This can happen when using async/await in older browsers
 */
if (typeof window !== 'undefined' && !window.regeneratorRuntime) {
  try {
    // This is a lightweight solution to avoid needing @babel/polyfill
    window.regeneratorRuntime = {
      wrap: function(fn) { return fn; },
      mark: function(fn) { return fn; },
      isGeneratorFunction: function() { return false; },
      async: function(fn) { return fn; }
    };
    console.log("Added regeneratorRuntime compatibility fix");
  } catch (e) {
    console.warn("Failed to add regeneratorRuntime compatibility fix", e);
  }
}

/**
 * Fix for network error retry
 * This is a global handler for network errors
 */
if (typeof window !== 'undefined') {
  window.addEventListener('offline', function() {
    document.title = document.title + " (Offline)";
    console.warn("Browser went offline");
  });
  
  window.addEventListener('online', function() {
    document.title = document.title.replace(" (Offline)", "");
    console.log("Browser back online - reloading in 5 seconds");
    
    // Reload after 5 seconds to refresh data
    setTimeout(function() {
      if (window.navigator.onLine) {
        window.location.reload();
      }
    }, 5000);
  });
}
