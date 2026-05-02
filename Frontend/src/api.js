// Central API configuration
// Change this one value to switch between dev and production backend.
export const API_BASE = "http://127.0.0.1:5000";

const promiseCache = new Map();

export const fetchRatingData = (username) => {
  const key = `rating_${username}`;
  if (!promiseCache.has(key)) {
    const p = fetch(`${API_BASE}/rating`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username }),
    }).then(res => res.json());
    promiseCache.set(key, p);
  }
  return promiseCache.get(key);
};

export const fetchRecommendedData = (username) => {
  const key = `rec_${username}`;
  if (!promiseCache.has(key)) {
    const p = fetch(`${API_BASE}/recommended`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username }),
    }).then(res => res.json());
    promiseCache.set(key, p);
  }
  return promiseCache.get(key);
};

export const fetchDashboardData = (username) => {
  const key = `dashboard_${username}`;

  if (!promiseCache.has(key)) {
    const p = fetch(`${API_BASE}/dashboard`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username }),
    }).then(async (res) => {
      if (!res.ok) {
        throw new Error("Failed to fetch dashboard data");
      }
      return res.json();
    });

    promiseCache.set(key, p);
  }

  return promiseCache.get(key);
};

// Help clear cache externally if the user wants to forcefully refresh
export const clearApiCache = (username) => {
  promiseCache.delete(`rating_${username}`);
  promiseCache.delete(`rec_${username}`);
  promiseCache.delete(`dashboard_${username}`);
};
