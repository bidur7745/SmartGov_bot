import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
// import emblem from '../assets/emblem_of_Nepal.png';
import emblem from "./assets/emblem_of_Nepal.png"

export default function First() {
  const [mobileNumber, setMobileNumber] = useState('');
  const [mpin, setMpin] = useState('');
  const navigate = useNavigate();

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!mobileNumber || !mpin) {
      alert('कृपया सबै आवश्यक फिल्डहरू भर्नुहोस् / Please fill all required fields');
      return;
    }
    navigate('/second');
  };

  return (
    <div className="min-h-screen bg-gray-100">
      {/* Header with emblem and government text */}
      <div className="bg-white border-b">
        <div className="max-w-4xl mx-auto flex items-center py-4 px-4">
          <img src={emblem} alt="Government of Nepal" className="w-16 h-16 mr-4" />
          <div>
            <p className="font-bold text-lg text-gray-800">Government of Nepal</p>
            <p className="text-sm text-blue-700">Ministry of Physical Infrastructure and Transport</p>
            <p className="text-base font-semibold text-gray-700">Department of Transport Management</p>
            <p className="text-base font-bold text-red-600">Online Driving License System</p>
          </div>
        </div>
      </div>

      {/* Navigation Bar */}
      <div className="bg-blue-700 text-white">
        <div className="max-w-4xl mx-auto flex space-x-6 px-4 h-12 items-center">
          <a href="/login" className="hover:underline">Home</a>
          <a href="/licensecheck" className="hover:underline">License Search</a>
          <a href="https://dotm.gov.np/DrivingLicense/SearchLicense" target="_blank" rel="noopener noreferrer" className="hover:underline">Print Check</a>
          <a href="https://dotm.gov.np/FAQ/MainIndex" target="_blank" rel="noopener noreferrer" className="hover:underline">FAQ</a>
          <a href="/assets/downloads/user_manual.pdf" target="_blank" rel="noopener noreferrer" className="hover:underline">Guide</a>
        </div>
      </div>

      {/* Main Content */}
      <div className="max-w-4xl mx-auto grid grid-cols-1 md:grid-cols-2 gap-8 py-10 px-4">
        {/* Left: Form */}
        <div className="bg-white rounded-lg shadow p-6 flex flex-col">
          <h2 className="text-lg font-semibold mb-4">Enter your own Mobile Number (आफ्नो मोबाइल नम्बर प्रविष्ट गर्नुहोस्)</h2>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <input
                type="text"
                value={mobileNumber}
                onChange={e => setMobileNumber(e.target.value.replace(/[^0-9]/g, ""))}
                placeholder="Mobile No"
                maxLength={10}
                className="w-full px-4 py-2 border border-gray-300 rounded focus:ring-2 focus:ring-blue-500 outline-none"
                required
              />
            </div>
            <div className="text-red-600 font-semibold text-sm mb-2">Important:</div>
            <div className="text-gray-700 text-sm mb-2">
              Please use the mobile number registered with your name to sign up. You are not allowed to change it afterward.<br />
              (यो अनलाईन फाराम भर्नका लागि प्रयोग गरिने मोबाईल नं. पछि परिवर्तन गर्न नमिल्ने भएकोले आफ्नै नाममा रहेको मोबाईल नं. मात्र प्रयोग गर्नुहोला ।)
            </div>
            <div>
              <input
                type="password"
                value={mpin}
                onChange={e => setMpin(e.target.value)}
                placeholder="MPIN (4-6 digits)"
                minLength={4}
                maxLength={6}
                className="w-full px-4 py-2 border border-gray-300 rounded focus:ring-2 focus:ring-blue-500 outline-none"
                required
              />
              <p className="text-gray-500 text-xs mt-1">MPIN should be 4-6 digits (MPIN ४-६ अंकको हुनुपर्छ)</p>
            </div>
            <button
              type="submit"
              className="w-full bg-blue-700 text-white py-2 rounded font-semibold hover:bg-blue-800 transition-colors"
            >
              Next
            </button>
          </form>
        </div>
        {/* Right: Instructions */}
        <div className="bg-white rounded-lg shadow p-6 overflow-y-auto">
          <h3 className="font-semibold text-gray-900 mb-2">अनलाइन आवेदन फाराम भर्ने लगायत अन्य सम्बन्धित विषय सम्बन्धी जानकारीहरु</h3>
          <p className="text-sm text-gray-700 mb-4">Instructions for filling online application form and others</p>
          <ol className="list-decimal list-inside space-y-2 text-sm text-gray-800">
            <li>
              नयाँ सवारी चालक अनुमतिपत्र तथा वर्ग थपका लागि यातायात व्यवस्था कार्यालय / यातायात व्यवस्था सेवा कार्यालयले विवरण रुजु एवंम् निवेदकको बायोमेट्रिक लिने कार्यहरु सार्वजनिक बिदा बाहेक हप्ताको प्रत्येक आइतबार, सोमबार, मंगलबार र बुधबारका दिन गर्ने गर्छ । यसका लागि निवेदकले यस प्रणालीमा आफ्नो निवेदक खाता बनाई प्रत्येक दिनको १५औं दिन अर्थात १६ दिनभित्र लाइसेन्सको वर्ग कोटा उपलब्ध भएको दिन सम्बन्धित कार्यालयमा अनलाइन आवेदन दर्ता गरी कार्यालय भिजिट डेट लिन सकिनेछ । तर प्रत्येक १६ औं दिनका लागि नयाँ आवेदन फाराम बिहान ७ बजे (शनिबार / आइतबार /सोमबार / मङ्गलबार) मात्र खुल्ला हुन्छ र कोटा नसकिएसम्म सातै दिन २४ घण्टासम्म फाराम भर्न सकिन्छ । निवेदकले आफ्नो निवेदक खाता एकभन्दा बढी बनाउनु हुँदैन ।
            </li>
            <li>
              अनलाइन आवेदन फाराम भर्दा निवेदकले आफ्नो मोवाइल नम्बर सहित अन्य विवरण सही प्रविष्ट गर्नु पर्दछ ।
            </li>
            <li>
              पहिचान परिचयपत्र (नागरिकता, पासपोर्ट र लाइसेन्स) को मूल स्क्यान गरिएको प्रतिलिपि अपलोड गर्नुपर्छ ।
            </li>
            <li>
              विवरण रुजु एवंम् बायोमेट्रिकका लागि प्राप्त गरेको कार्यालय भिजिट डेटमा निवेदक उपस्थित हुन नसकेको अवस्थामा सो मितिबाट १५ दिन पछि मात्र पुनः अनलाइन आवेदन भर्न सक्नेछ ।
            </li>
            <li>
              दर्ता गरिएको अनलाइन आवेदन फाराममा रहेको व्यक्तिगत विवरण जस्तै नाम, थर, नागरिकता विवरण, मोबाइल नं. र जन्म मिति मा कुनै त्रुटि भएमा उक्त फाराम रद्द हुनेछ । साथै वर्ग थपको लागि फाराम भर्दा प्राप्त गरिसकेको लाइसेन्सको वर्ग गलत प्रविष्ट भएमा पनि फाराम रद्द हुनेछ ।
            </li>
            <li>
              सवारी चालक अनुमतिपत्रका लागि निवेदकको उमेर दुई पाङ्ग्रे सवारी (वर्ग A/K) को लागि १६ वर्ष, साना सवारी (वर्ग B) को लागि १८ वर्ष र अन्य सवारीका लागि २१ वर्ष पूरा भएको हुनुपर्नेछ ।
            </li>
            <li>
              सवारी चालकको स्मार्ट-कार्ड सवारी चालक अनुमतिपत्र सम्बन्धी विवरण <a className="text-blue-700 underline" href="https://applydl.dotm.gov.np/license-check" target="_blank" rel="noopener noreferrer">license search</a> मा क्लिक गरी हेर्न सकिन्छ ।
            </li>
            <li>
              ट्रायल परीक्षामा असफल भएका परीक्षार्थीहरुले असफल भएको प्रथम मितिले ९० दिनाभित्र बढीमा ३ पटक सम्म रि-ट्रायल दिन सक्नेछन् ।
            </li>
            <li>
              लाइसेन्स वर्ग पावरटिलर (D), ट्र्रयाक्टर (E), मिनिबस, ट्रक तथा बस (F, G) प्राप्त गरेका सवारी चालकले कुनैपनि अर्को वर्ग थप गर्दा लिखित परीक्षा अनिवार्य दिनुपर्दछ ।
            </li>
            <li>
              बायोमेट्रिक दर्ता, लिखित तथा प्रयोगात्मक परीक्षाका लागि सम्बन्धित कार्यालयमा जाँदा अनिवार्य रूपमा सक्कल नागरिकता, सक्कल लाइसेन्स (वर्ग थपको हकमा) साथै लिएर मात्र जानुपर्छ ।
            </li>
            <li>
              प्रयोगात्मक परीक्षाका दिन परीक्षार्थीले अनिवार्य रूपमा जुत्ता लगाई आउनुपर्छ । साथै लिखित तथा प्रयोगात्मक परीक्षा केन्द्रहरुमा मोबाइल फोन निषेध गरिएको छ ।
            </li>
            <li>
              आफ्नो स्मार्ट-कार्ड सवारी चालक अनुमतिपत्र छपाई भए/नभएको बारेमा जानकारीका लागि <a className="text-blue-700 underline" href="https://dotm.gov.np/DrivingLicense/SearchLicense" target="_blank" rel="noopener noreferrer">license print check</a> क्लिक गरी जानकारी प्राप्त गर्न सकिन्छ ।
            </li>
          </ol>
        </div>
      </div>
    </div>
  );
}