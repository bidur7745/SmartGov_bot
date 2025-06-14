import React, { useEffect, useState } from 'react';

const generateDLId = () => {
  // Generate a random 6-digit number
  const randomNum = Math.floor(100000 + Math.random() * 900000);
  return `DL-${randomNum}`;
};

const Formsubmit = () => {
  const [dlId, setDlId] = useState('');

  useEffect(() => {
    setDlId(generateDLId());
  }, []);

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gray-100">
      <div className="bg-white shadow-lg rounded-lg p-8 max-w-md w-full text-center">
        <h2 className="text-2xl font-bold text-green-700 mb-4">Application Submitted Successfully!</h2>
        <p className="text-lg text-gray-700 mb-2">Thank you for your submission.</p>
        <p className="text-gray-600 mb-6">Your application has been received and is being processed.</p>
        <div className="bg-green-100 border border-green-400 text-green-800 rounded px-4 py-3 mb-4">
          <span className="font-semibold">Your Reference ID:</span>
          <div className="text-xl font-mono mt-2">{dlId}</div>
        </div>
        <p className="text-gray-500 text-sm">Please save this ID for future reference.</p>
      </div>
    </div>
  );
};

export default Formsubmit;
