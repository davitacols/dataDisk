export default function Services() {
  return (
    <div className="pt-16 py-20">
      <div className="max-w-6xl mx-auto px-4">
        <h1 className="text-4xl font-bold text-gray-900 mb-8 text-center">Our Services</h1>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          <div className="bg-white p-8 rounded-lg shadow-lg">
            <h2 className="text-2xl font-semibold mb-4">Web Development</h2>
            <p className="text-gray-600">Modern, responsive websites built with the latest technologies.</p>
          </div>
          <div className="bg-white p-8 rounded-lg shadow-lg">
            <h2 className="text-2xl font-semibold mb-4">Mobile Apps</h2>
            <p className="text-gray-600">Native and cross-platform mobile applications.</p>
          </div>
          <div className="bg-white p-8 rounded-lg shadow-lg">
            <h2 className="text-2xl font-semibold mb-4">Machine Learning</h2>
            <p className="text-gray-600">AI-powered solutions for business automation.</p>
          </div>
          <div className="bg-white p-8 rounded-lg shadow-lg">
            <h2 className="text-2xl font-semibold mb-4">Tech Consulting</h2>
            <p className="text-gray-600">Strategic guidance for digital transformation.</p>
          </div>
        </div>
      </div>
    </div>
  )
}