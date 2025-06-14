import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import image from './assets/emblem_of_Nepal.png'

export default function Second() {
  const [form, setForm] = useState({
    firstName: '',
    middleName: '',
    lastName: '',
    dob: '',
    citizenshipNo: '',
    issuedDistrictType: 'zonal',
    issuedDistrict: '',
    issuedDate: '',
    email: '',
  });
  const navigate = useNavigate();

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm((prev) => ({ ...prev, [name]: value }));
  };

  const handleRadioChange = (e) => {
    setForm((prev) => ({ ...prev, issuedDistrictType: e.target.value, issuedDistrict: '' }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    // Add validation or navigation here
    navigate('/formsubmit');
  };

  return (
    <div className="min-h-screen bg-gray-100 flex flex-col items-center py-8">
      <div className="w-full max-w-5xl bg-white rounded-xl shadow p-8">
        <div className="flex flex-col items-center mb-6">
          <img src={image} alt="Nepal Emblem" className="w-20 h-20 mb-2" />
          <div className="text-center">
            <p className="font-bold text-gray-800">Government of Nepal</p>
            <p className="text-blue-700 text-sm">Ministry of Physical Infrastructure and Transport</p>
            <p className="font-semibold text-gray-700 text-base">Department of Transport Management</p>
            <p className="font-bold text-red-600 text-base">Online Driving License System</p>
          </div>
        </div>
        <h2 className="text-2xl font-semibold mb-2">Enter your Personal Details</h2>
        <p className="font-semibold text-black mb-6">(Please check and enter your details correctly. You will not be allowed to modify the details later.)</p>
        <form onSubmit={handleSubmit} className="bg-gray-50 border rounded-lg p-6">
          <fieldset>
            <legend className="font-semibold text-lg mb-4">A. Citizenship Details ( नागरिकताको विवरण )</legend>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
              <div>
                <label className="block text-sm font-medium mb-1">First Name in English (पहिलो नाम) <span className="text-red-500">*</span></label>
                <input name="firstName" value={form.firstName} onChange={handleChange} placeholder="First Name" className="w-full px-3 py-2 border rounded" required />
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">Middle Name in English (बीचको नाम)</label>
                <input name="middleName" value={form.middleName} onChange={handleChange} placeholder="Middle Name" className="w-full px-3 py-2 border rounded" />
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">Last Name in English (थर) <span className="text-red-500">*</span></label>
                <input name="lastName" value={form.lastName} onChange={handleChange} placeholder="Last Name" className="w-full px-3 py-2 border rounded" required />
              </div>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
              <div>
                <label className="block text-sm font-medium mb-1">Date of Birth (B.S.) (जन्म मिति बि.सं.) <span className="text-red-500">*</span></label>
                <input name="dob" value={form.dob} onChange={handleChange} placeholder="YYYY-MM-DD" className="w-full px-3 py-2 border rounded" required />
              </div>
              <div className="md:col-span-2">
                <label className="block text-sm font-medium mb-1">Citizenship No. (नागरिकता नं.) (Enter English Number) <span className="text-red-500">*</span></label>
                <input name="citizenshipNo" value={form.citizenshipNo} onChange={handleChange} placeholder="Eg:37-02-75-1111 or 12334/2323 (Please enter - or / as on citizenshipno)" className="w-full px-3 py-2 border rounded" required />
              </div>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4 items-end">
              <div className="md:col-span-2">
                <label className="block text-sm font-medium mb-1">Issued District (जारी जिल्ला) <span className="text-red-500">*</span></label>
                <div className="flex items-center space-x-4 mb-2">
                  <label className="flex items-center">
                    <input type="radio" name="issuedDistrictType" value="zonal" checked={form.issuedDistrictType === 'zonal'} onChange={handleRadioChange} className="mr-1" />
                    Zonal (अञ्चल)
                  </label>
                  <label className="flex items-center">
                    <input type="radio" name="issuedDistrictType" value="provincial" checked={form.issuedDistrictType === 'provincial'} onChange={handleRadioChange} className="mr-1" />
                    Provincial (प्रदेश)
                  </label>
                </div>
                <input name="issuedDistrict" value={form.issuedDistrict} onChange={handleChange} placeholder="Select District" className="w-full px-3 py-2 border rounded" required />
              </div>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
              <div>
                <label className="block text-sm font-medium mb-1">Issued Date (जारी मिति) <span className="text-red-500">*</span></label>
                <input name="issuedDate" value={form.issuedDate} onChange={handleChange} placeholder="Issue Date" className="w-full px-3 py-2 border rounded" required />
              </div>
              <div className="md:col-span-2">
                <label className="block text-sm font-medium mb-1">Email (इमेल)</label>
                <input name="email" value={form.email} onChange={handleChange} placeholder="Email Address" className="w-full px-3 py-2 border rounded" />
              </div>
            </div>
          </fieldset>
          <div className="flex justify-center gap-4 mt-6">
            <button type="button" className="bg-blue-700 text-white px-8 py-2 rounded font-semibold hover:bg-blue-800 transition-colors">BACK</button>
            <button type="submit" className="bg-blue-700 text-white px-8 py-2 rounded font-semibold hover:bg-blue-800 transition-colors">Next</button>
          </div>
        </form>
      </div>
    </div>
  );
}
