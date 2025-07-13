console.log("Starting MQTT Dashboard script...");

const client = mqtt.connect('ws://192.168.0.106:9001');

let latestData = {
    temperature: "--",
    humidity: "--",
    light: "--",
    sound: "--",
    motion: "--",
    planType: "--"
};

let lastUpdateTime = 0;

client.on('connect', () => {
    console.log("? MQTT connected to ws://192.168.0.106:9001");
    client.subscribe('building/sensors/#', (err) => {
        if (err) {
            console.error("Subscription error:", err);
        } else {
            console.log("Subscribed to building/sensors/#");
        }
    });
});

client.on('message', (topic, message) => {
    const val = message.toString();

    if (topic.endsWith("temperature")) {
        latestData.temperature = val;
    } else if (topic.endsWith("humidity")) {
        latestData.humidity = val;
    } else if (topic.endsWith("light")) {
        latestData.light = val;
    } else if (topic.endsWith("sound")) {
        latestData.sound = val;
    } else if (topic.endsWith("motion")) {
        latestData.motion = (val === "1" ? "Yes" : "No");
    } else if (topic.endsWith("plan_type")) {
        latestData.planType = val;
    }

    const now = Date.now();
    if (now - lastUpdateTime >= 500) { // 0.5s throttle
        updateDashboard();
        lastUpdateTime = now;
    }
});

function updateDashboard() {
    document.getElementById("temperature").innerText = latestData.temperature;
    document.getElementById("humidity").innerText = latestData.humidity;
    document.getElementById("light").innerText = 
        latestData.light !== "--" ? parseInt(latestData.light) + "%" : "--";
    document.getElementById("sound").innerText = latestData.sound;
    document.getElementById("motion").innerText = latestData.motion;

    const el = document.getElementById("aiDecision");
    el.innerText = latestData.planType;

    if (latestData.planType === "SAFE PLAN") {
        el.style.color = "green";
    } else if (latestData.planType === "ALERT PLAN" || latestData.planType === "FIRE PLAN") {
        el.style.color = "red";
    } else {
        el.style.color = "#333";
    }
}

client.on('error', (err) => {
    console.error("MQTT connection error:", err);
});
