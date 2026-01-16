# FitTrack Web Application

A simple and clean web interface for the FitTrack Gym Management System.

## 📁 Project Structure

```
web-app/
├── main.py                 # FastAPI application (serves the frontend)
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── templates/             # HTML templates
│   └── index.html        # Main page
└── static/               # Static files
    ├── css/
    │   └── styles.css    # All CSS styles
    └── js/
        ├── config.js     # Configuration settings
        ├── api.js        # API service (handles backend calls)
        └── app.js        # Main application logic
```

## 🚀 Getting Started

### 1. Install Dependencies

```bash
cd web-app
pip install -r requirements.txt
```

### 2. Make Sure Backend is Running

The backend API should be running on port 5000:

```bash
cd ../server
python app.py
```

### 3. Run the Web Application

```bash
python main.py
```

The web app will start on **http://localhost:8000**

## 📖 How It Works

### Backend (FastAPI)
- **main.py**: Simple FastAPI server that serves the HTML and static files
- Runs on port 8000
- Serves the frontend interface

### Frontend (HTML/CSS/JavaScript)

#### HTML (templates/index.html)
- Main structure of the webpage
- Contains sections for Members, Classes, Plans, and Check-ins
- Includes forms for adding new data

#### CSS (static/css/styles.css)
- All styling for the application
- Responsive design (works on mobile and desktop)
- Clean, modern look with cards and animations

#### JavaScript Files:

1. **config.js**
   - Configuration settings
   - API URL (points to backend on port 5000)
   - Easy to modify if backend URL changes

2. **api.js**
   - Handles all communication with the backend
   - Methods for GET, POST, PUT, DELETE requests
   - Easy-to-use API wrapper

3. **app.js**
   - Main application logic
   - Handles user interactions
   - Updates the UI with data from backend
   - Form handling and validation

## 🎯 Features

- **Members Management**: View all members, add new members
- **Classes View**: See all gym classes and schedules
- **Plans View**: Browse membership plans
- **Check-ins**: View recent gym check-ins
- **Responsive Design**: Works on all screen sizes
- **Clean UI**: Modern, easy-to-understand interface

## 🔧 Configuration

To change the backend API URL, edit `static/js/config.js`:

```javascript
const CONFIG = {
    API_BASE_URL: 'http://127.0.0.1:5000/api',  // Change this if needed
    // ...
};
```

## 📝 Code Structure (For Students)

### Understanding the Flow:

1. **User opens browser** → FastAPI serves `index.html`
2. **Page loads** → JavaScript files load (`config.js`, `api.js`, `app.js`)
3. **App initializes** → Fetches data from backend API
4. **User interacts** → JavaScript handles events and updates UI
5. **API calls** → `api.js` communicates with backend on port 5000

### Key Concepts:

- **Separation of Concerns**: HTML (structure), CSS (style), JavaScript (behavior)
- **API Service Pattern**: All backend calls in one place (`api.js`)
- **Event-Driven**: User actions trigger functions
- **Async/Await**: Modern way to handle API calls

## 🐛 Troubleshooting

**Problem**: Can't load data
- **Solution**: Make sure backend is running on port 5000

**Problem**: Port 8000 already in use
- **Solution**: Change port in `main.py` (line 30)

**Problem**: CORS errors
- **Solution**: Backend needs to allow requests from port 8000

## 💡 Tips for Students

1. **Start Simple**: Look at one file at a time
2. **Use Browser DevTools**: Press F12 to see console logs and network requests
3. **Read Comments**: Code has helpful comments explaining each part
4. **Test Changes**: Refresh browser after making changes
5. **Check Console**: Look for error messages in browser console

## 🎨 Customization

Want to change colors? Edit `static/css/styles.css`:
- Main purple color: `#667eea` (change this for different theme)
- Background: `#f5f5f5`
- Text: `#333`

## 📚 Learning Resources

- **FastAPI**: https://fastapi.tiangolo.com/
- **HTML**: https://developer.mozilla.org/en-US/docs/Web/HTML
- **CSS**: https://developer.mozilla.org/en-US/docs/Web/CSS
- **JavaScript**: https://developer.mozilla.org/en-US/docs/Web/JavaScript

---

**Happy Coding! 💪**
