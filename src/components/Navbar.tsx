'use client'

import Link from 'next/link'
import { useState } from 'react'

export default function Navbar() {
  const [isOpen, setIsOpen] = useState(false)

  return (
    <nav className="bg-white shadow-lg fixed w-full z-50">
      <div className="max-w-7xl mx-auto px-4">
        <div className="flex justify-between h-16">
          <div className="flex items-center">
            <Link href="/" className="text-2xl font-bold text-primary-600">
              dataDisk
            </Link>
          </div>
          
          <div className="hidden md:flex items-center space-x-8">
            <Link href="/" className="text-gray-700 hover:text-primary-600">Home</Link>
            <Link href="/about" className="text-gray-700 hover:text-primary-600">About</Link>
            <Link href="/services" className="text-gray-700 hover:text-primary-600">Services</Link>
            <Link href="/projects" className="text-gray-700 hover:text-primary-600">Projects</Link>
            <Link href="/contact" className="bg-primary-600 text-white px-4 py-2 rounded-lg hover:bg-primary-700">
              Contact
            </Link>
          </div>

          <div className="md:hidden flex items-center">
            <button onClick={() => setIsOpen(!isOpen)} className="text-gray-700">
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d={isOpen ? "M6 18L18 6M6 6l12 12" : "M4 6h16M4 12h16M4 18h16"} />
              </svg>
            </button>
          </div>
        </div>

        {isOpen && (
          <div className="md:hidden">
            <div className="px-2 pt-2 pb-3 space-y-1">
              <Link href="/" className="block px-3 py-2 text-gray-700">Home</Link>
              <Link href="/about" className="block px-3 py-2 text-gray-700">About</Link>
              <Link href="/services" className="block px-3 py-2 text-gray-700">Services</Link>
              <Link href="/projects" className="block px-3 py-2 text-gray-700">Projects</Link>
              <Link href="/contact" className="block px-3 py-2 text-gray-700">Contact</Link>
            </div>
          </div>
        )}
      </div>
    </nav>
  )
}