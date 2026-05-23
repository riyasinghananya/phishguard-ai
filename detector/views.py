from django.shortcuts import render
import joblib
import re

# Load ML model
model = joblib.load("phishing_model.pkl")


def home(request):

    result = ""
    score = 0
    safe_score = 0
    phishing_score = 0

    if request.method == "POST":

        url = request.POST.get("url")

        # -----------------------------
        # Fake Brand / Typo Detection
        # -----------------------------

        fake_brands = [
            "goog1e",
            "g00gle",
            "paypa1",
            "faceb00k",
            "arnazon",
            "micr0soft",
            "instagrarn"
        ]

        typo_detected = any(
            word in url.lower()
            for word in fake_brands
        )

        # -----------------------------
        # Features
        # -----------------------------

        having_at = 1 if "@" in url else 0

        having_ip = 1 if re.search(
            r"\d+\.\d+\.\d+\.\d+",
            url
        ) else 0

        path = 1 if "/" in url else 0

        prefix_suffix = 1 if "-" in url else 0

        protocol = 1 if "https" in url else 0

        redirection = 1 if "//" in url[8:] else 0

        sub_domains = url.count(".")

        url_length = len(url)

        age_domain = 0

        dns_record = 1

        domain_registration_length = 1

        http_tokens = 1 if "http" in url.replace(
            "https://",
            ""
        ) else 0

        statistical_report = 0

        tiny_url = 1 if (
            "bit.ly" in url or
            "tinyurl" in url
        ) else 0

        # -----------------------------
        # ML Features
        # -----------------------------

        features = [[
            having_at,
            having_ip,
            path,
            prefix_suffix,
            protocol,
            redirection,
            sub_domains,
            url_length,
            age_domain,
            dns_record,
            domain_registration_length,
            http_tokens,
            statistical_report
        ]]

        # -----------------------------
        # Prediction
        # -----------------------------

        prediction = model.predict(features)[0]

        confidence = model.predict_proba(features)[0]

        safe_score = round(confidence[0] * 100)

        phishing_score = round(confidence[1] * 100)

        # -----------------------------
        # Final Result
        # -----------------------------

        if prediction == 1 or typo_detected:

            result = "⚠️ Dangerous Website"

            score = 95

        else:

            result = "✅ Safe Website"

            score = 10

    return render(request, "home.html", {
        "result": result,
        "score": score,
        "safe_score": safe_score,
        "phishing_score": phishing_score
    })