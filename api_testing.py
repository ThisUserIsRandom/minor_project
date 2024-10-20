import google.generativeai as genai
#AIzaSyBVZ4t-A7M_AlkgeBRlRznH6sr-GUjO4mo
def test_api(key,data="0"):
    genai.configure(api_key=key)

    model = genai.GenerativeModel("gemini-1.5-flash")

    try:
        response = model.generate_content(data)
        if data=="0":
            return 1
        else:
            return response
    except Exception as e:
        return 0
