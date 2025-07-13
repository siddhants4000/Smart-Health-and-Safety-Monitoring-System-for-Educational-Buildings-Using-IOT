// Make sure this is inside your static folder
console.log("Starting MQTT Dashboard script...");

const client = mqtt.connect('ws://192.168.0.106:9001');

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
    console.log(`Topic: ${topic}, Message: ${val}`);

    if (topic.endsWith("temperature")) {
        document.getElementById("temperature").innerText = val;
    } else if (topic.endsWith("humidity")) {
        document.getElementById("humidity").innerText = val;
    } else if (topic.endsWith("light")) {
        document.getElementById("light").innerText = val;
    } else if (topic.endsWith("sound")) {
        document.getElementById("sound").innerText = val;
    } else if (topic.endsWith("motion")) {
        document.getElementById("motion").innerText = (val === "1" ? "Yes" : "No");
    } else if (topic.endsWith("ai_decision")) {
        const el = document.getElementById("aiDecision");
        if (val === "ON") {
            el.innerText = "ON (Triggered)";
            el.style.color = "green";
        } else {
            el.innerText = "OFF";
            el.style.color = "red";
        }
    }
});

client.on('error', (err) => {
    console.error("MQTT connection error:", err);
});