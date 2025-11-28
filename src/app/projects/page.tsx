export default function Projects() {
  return (
    <div className="pt-16 py-20">
      <div className="max-w-6xl mx-auto px-4">
        <h1 className="text-4xl font-bold text-gray-900 mb-8 text-center">Our Projects</h1>
        <p className="text-lg text-gray-600 text-center mb-12">
          Explore our portfolio of successful projects and client solutions.
        </p>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {[1, 2, 3, 4, 5, 6].map((item) => (
            <div key={item} className="bg-white rounded-lg shadow-lg overflow-hidden">
              <div className="h-48 bg-gray-200"></div>
              <div className="p-6">
                <h3 className="text-xl font-semibold mb-2">Project {item}</h3>
                <p className="text-gray-600">Description of project and technologies used.</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}