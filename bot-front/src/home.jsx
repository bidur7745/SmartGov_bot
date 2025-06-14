export default function Home() {


  return (
    <>
      {/* Font Awesome CDN */}
      <link 
        rel="stylesheet" 
        href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css"
        integrity="sha512-iecdLmaskl7CVkqkXNQ/ZH/XLlvWZOJyj7Yy7tcenmpD1ypASozpmT/E0iPtmFIB46ZmdtAc9eNBvH0H/ZpiBw=="
        crossOrigin="anonymous"
        referrerPolicy="no-referrer"
      />
      <div className="min-h-screen bg-gray-50 text-gray-800">
      {/* Header */}
      <header className="bg-blue-600 text-white py-6 text-center">
        <h1 className="text-3xl font-bold mb-2">SmartGov Bot</h1>
        <p className="text-blue-100">Your guide to Nepali government services, made simple.</p>
      </header>

      {/* Main Container */}
      <div className="max-w-4xl mx-auto px-6 py-8">
        {/* Hero Section */}
        <div className="text-center mb-8">
          <h2 className="text-2xl font-semibold mb-4 text-gray-900">
            Apply for Documents, Get Info, or Talk to Our Bot
          </h2>
          <p className="text-gray-600 text-lg">
            We help you with services like Passport, PAN, Driving License, Loksewa exams, and more.
          </p>
        </div>

        {/* Services Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
          <div className="bg-white p-6 rounded-lg shadow-md hover:shadow-lg transition-shadow">
            <h3 className="text-xl font-semibold mb-3 flex items-center">
              <i className="fas fa-file-alt text-blue-600 mr-3 text-2xl"></i>
              Document Services
            </h3>
            <p className="text-gray-600">
              Citizenship, Passport, PAN, Driving License
            </p>
          </div>

          <div className="bg-white p-6 rounded-lg shadow-md hover:shadow-lg transition-shadow">
            <h3 className="text-xl font-semibold mb-3 flex items-center">
              <i className="fas fa-graduation-cap text-green-600 mr-3 text-2xl"></i>
              Loksewa Support
            </h3>
            <p className="text-gray-600">
              Get updates and exam info directly from the bot
            </p>
          </div>

          <div className="bg-white p-6 rounded-lg shadow-md hover:shadow-lg transition-shadow">
            <h3 className="text-xl font-semibold mb-3 flex items-center">
              <i className="fas fa-comments text-purple-600 mr-3 text-2xl"></i>
              Voice/Text Chat
            </h3>
            <p className="text-gray-600">
              Talk naturally or type — we support both
            </p>
          </div>

          <div className="bg-white p-6 rounded-lg shadow-md hover:shadow-lg transition-shadow">
            <h3 className="text-xl font-semibold mb-3 flex items-center">
              <i className="fas fa-hands-helping text-orange-600 mr-3 text-2xl"></i>
              Social Support
            </h3>
            <p className="text-gray-600">
              Old Age Pension, Widow, Disability services
            </p>
          </div>
        </div>

        {/* Chat Button */}
        <div className="text-center">
          <button
            onClick={() => window.location.href='/chatbot'}
            className="bg-green-600 hover:bg-green-700 text-white font-semibold py-4 px-8 rounded-lg text-lg transition-colors duration-200 shadow-md hover:shadow-lg inline-flex items-center"
          >
            <i className="fas fa-comment-dots mr-2"></i>
            Start Chatting
          </button>
        </div>
      </div>

      {/* Footer */}
      <footer className="text-center mt-12 py-6 text-gray-500 text-sm">
        Made with <i className="fas fa-heart text-red-500"></i> by Team SmartGov • Contact us for suggestions
      </footer>
    </div>
  </>
  );
}