import store from './store.js';

export default function fetchUtil({ endpoint, method = 'GET', headers = {}, data = null }) {
  const fullUrl = `http://127.0.0.1:5000/api/${endpoint}`;

  return new Promise(async (resolve, reject) => {
    try {
      const response = await fetch(fullUrl, {
        method,
        headers: {
          ...headers,
        },
        body: data ? JSON.stringify(data) : undefined,
      });

      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }

      const responseData = await response.json();
      resolve(responseData);
    } catch (error) {
      reject(error);
    }
  });
}
