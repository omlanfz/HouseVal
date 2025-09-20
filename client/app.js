// Use environment variable for API URL or fallback to localhost for development
const API_BASE_URL = "https://houseval.onrender.com";

function getBathValue() {
  const uiBathrooms = document.getElementsByName("uiBathrooms");
  for (let i = 0; i < uiBathrooms.length; i++) {
    if (uiBathrooms[i].checked) {
      return parseInt(uiBathrooms[i].value);
    }
  }
  return -1;
}

function getBedsValue() {
  const uiBHK = document.getElementsByName("uiBHK");
  for (let i = 0; i < uiBHK.length; i++) {
    if (uiBHK[i].checked) {
      return parseInt(uiBHK[i].value);
    }
  }
  return -1;
}

async function onClickedEstimatePrice() {
  console.log("Estimate price button clicked");
  const sqft = document.getElementById("uiSqft");
  const beds = getBedsValue();
  const bathrooms = getBathValue();
  const location = document.getElementById("uiLocations");
  const estPrice = document.getElementById("uiEstimatedPrice");

  if (
    isNaN(parseFloat(sqft.value)) ||
    beds === -1 ||
    bathrooms === -1 ||
    location.value === ""
  ) {
    estPrice.innerHTML = `<h2 class='text-red-500 text-center font-bold'>Please fill all fields correctly.</h2>`;
    return;
  }

  const url = `${API_BASE_URL}/predict_home_price`;
  estPrice.innerHTML = `<h2 class='text-green-400 text-center font-bold animate-pulse'>Estimating...</h2>`;

  try {
    const response = await fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        total_sqft: parseFloat(sqft.value),
        beds: beds,
        bath: bathrooms,
        location: location.value,
      }),
    });

    const data = await response.json();

    if (response.ok) {
      if (data && data.estimated_price !== undefined) {
        // Format price with commas
        const formattedPrice = new Intl.NumberFormat("en-BD").format(
          data.estimated_price
        );
        estPrice.innerHTML = `<h2 class='text-3xl text-center font-bold text-green-400'>${formattedPrice} BDT</h2>`;
      } else {
        estPrice.innerHTML = `<h2 class='text-red-500 text-center font-bold'>Unexpected response from server.</h2>`;
      }
    } else {
      estPrice.innerHTML = `<h2 class='text-red-500 text-center font-bold'>Error: ${
        data.error || "Request failed"
      }</h2>`;
    }
  } catch (error) {
    console.error("Request failed:", error);
    estPrice.innerHTML = `<h2 class='text-red-500 text-center font-bold'>Failed to connect to server. Please try again later.</h2>`;
  }
}

async function onPageLoad() {
  console.log("document loaded");
  const url = `${API_BASE_URL}/get_location_names`;

  try {
    const response = await fetch(url);
    if (!response.ok) {
      throw new Error("Network response was not ok");
    }
    const data = await response.json();
    console.log("Response for get_location_names:", data);

    if (data && data.locations) {
      const locations = data.locations;
      const uiLocations = document.getElementById("uiLocations");
      uiLocations.innerHTML = `<option value="" disabled selected>Choose a Location</option>`;

      locations.forEach((location) => {
        const option = document.createElement("option");
        option.value = location;
        option.textContent = location;
        uiLocations.appendChild(option);
      });
    }
  } catch (error) {
    console.error("Failed to fetch location names:", error);
  }
}

window.onload = onPageLoad;
