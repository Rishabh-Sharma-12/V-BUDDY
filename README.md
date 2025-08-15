# V-BUDDY

V-BUDDY is a Python-based AI voice assistant powered by Llama. It acts as your personal voice buddy, providing intelligent responses and performing several useful tasks like generating QR codes and fetching live weather information.

## Features

- **Voice Assistant:** Powered by Llama, V-BUDDY can understand your voice commands and respond intelligently.
- **QR Code Generator:** Instantly generate QR codes for any text or URL.
- **Live Weather Fetching:** Get real-time weather updates for any location.
- **Easy Setup:** Just configure your API keys in a `.env` file and you're ready to go!

## Requirements

- Python 3.7+
- [Llama](https://github.com/facebookresearch/llama) (Ensure appropriate licensing and installation)
- Required Python libraries (see `requirements.txt`)

## Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Rishabh-Sharma-12/V-BUDDY.git
   cd V-BUDDY
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Create a `.env` file in the project root directory:**

   This file should contain your API keys for the required services. For example:
   ```
   OPENWEATHER_API_KEY=your_openweather_api_key_here
   LLAMA_API_KEY=your_llama_api_key_here
   ```

   - Replace `your_openweather_api_key_here` with your actual API key from [OpenWeather](https://openweathermap.org/api).
   - Replace `your_llama_api_key_here` with your Llama API key or access credentials.

4. **Run the application:**
   ```bash
   python main.py
   ```

## Usage

- **Voice Commands:** Interact with V-BUDDY using your voice to ask questions, generate QR codes, or get weather updates.
- **QR Code Generation:** Say or type a command to generate a QR code for a specific text or URL.
- **Weather Fetch:** Ask for the weather in a specific city or location.

## Example Commands

- “What’s the weather in New York?”
- “Generate a QR code for https://github.com”
- “Tell me a joke.”

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for improvements, new features, or bug fixes.

## License

This project is licensed under the MIT License.

---

**Note:** Make sure to use your own API keys and keep your `.env` file secure. Never share your API keys publicly.

---

> **Stay tuned for more updates and functionalities! We're actively working on adding new features—please wait for updates coming soon!**
