import { useState, useEffect } from 'react'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

function App() {
  const [user, setUser] = useState(null)
  const [token, setToken] = useState(localStorage.getItem('token'))
  const [notes, setNotes] = useState([])
  const [isFormOpen, setIsFormOpen] = useState(false)
  const [editingNote, setEditingNote] = useState(null)
  const [searchTerm, setSearchTerm] = useState('')
  const [uploadingPhotos, setUploadingPhotos] = useState(false)
  const [loginEmail, setLoginEmail] = useState('')
  const [formData, setFormData] = useState({
    wine_name: '',
    vintage: '',
    varietal: '',
    region: '',
    producer: '',
    color: 'Red',
    rating: '',
    tasting_date: '',
    price: '',
    appearance: '',
    aroma: '',
    taste: '',
    finish: '',
    food_pairing: '',
    notes: '',
    drinking_with: '',
    meal_type: '',
    photos: []
  })

  // Check authentication on mount
  useEffect(() => {
    if (token) {
      fetchNotes()
    }
  }, [token])

  const handleDemoLogin = async (e) => {
    e.preventDefault()
    try {
      const response = await fetch(`${API_URL}/api/auth/demo-login?email=${loginEmail}`, {
        method: 'POST',
      })
      const data = await response.json()
      setToken(data.access_token)
      setUser(data.user)
      localStorage.setItem('token', data.access_token)
    } catch (error) {
      console.error('Login error:', error)
      alert('Login failed. Please try again.')
    }
  }

  const handleLogout = () => {
    setToken(null)
    setUser(null)
    setNotes([])
    localStorage.removeItem('token')
  }

  const fetchNotes = async () => {
    if (!token) return
    
    try {
      const response = await fetch(`${API_URL}/api/notes`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      })
      if (response.ok) {
        const data = await response.json()
        // Handle photos for SQLite (stored as JSON string)
        const processedNotes = data.map(note => ({
          ...note,
          photos: typeof note.photos === 'string' ? JSON.parse(note.photos || '[]') : note.photos || []
        }))
        setNotes(processedNotes)
      } else if (response.status === 401) {
        handleLogout()
      }
    } catch (error) {
      console.error('Error fetching notes:', error)
    }
  }

  const handleInputChange = (e) => {
    const { name, value } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: value
    }))
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    
    try {
      const url = editingNote 
        ? `${API_URL}/api/notes/${editingNote.id}`
        : `${API_URL}/api/notes`
      
      const method = editingNote ? 'PUT' : 'POST'
      
      const response = await fetch(url, {
        method,
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          ...formData,
          vintage: formData.vintage ? parseInt(formData.vintage) : null,
          rating: formData.rating ? parseFloat(formData.rating) : null,
          price: formData.price ? parseFloat(formData.price) : null,
        }),
      })

      if (response.ok) {
        fetchNotes()
        resetForm()
      }
    } catch (error) {
      console.error('Error saving note:', error)
    }
  }

  const handleEdit = (note) => {
    setEditingNote(note)
    setFormData({
      wine_name: note.wine_name || '',
      vintage: note.vintage || '',
      varietal: note.varietal || '',
      region: note.region || '',
      producer: note.producer || '',
      color: note.color || 'Red',
      rating: note.rating || '',
      tasting_date: note.tasting_date || '',
      price: note.price || '',
      appearance: note.appearance || '',
      aroma: note.aroma || '',
      taste: note.taste || '',
      finish: note.finish || '',
      food_pairing: note.food_pairing || '',
      notes: note.notes || '',
      drinking_with: note.drinking_with || '',
      meal_type: note.meal_type || '',
      photos: note.photos || []
    })
    setIsFormOpen(true)
  }

  const handleDelete = async (id) => {
    if (window.confirm('Are you sure you want to delete this note?')) {
      try {
        await fetch(`${API_URL}/api/notes/${id}`, {
          method: 'DELETE',
          headers: {
            'Authorization': `Bearer ${token}`
          }
        })
        fetchNotes()
      } catch (error) {
        console.error('Error deleting note:', error)
      }
    }
  }

  const resetForm = () => {
    setFormData({
      wine_name: '',
      vintage: '',
      varietal: '',
      region: '',
      producer: '',
      color: 'Red',
      rating: '',
      tasting_date: '',
      price: '',
      appearance: '',
      aroma: '',
      taste: '',
      finish: '',
      food_pairing: '',
      notes: '',
      drinking_with: '',
      meal_type: '',
      photos: []
    })
    setEditingNote(null)
    setIsFormOpen(false)
  }

  const handlePhotoUpload = async (e) => {
    const files = e.target.files
    if (!files || files.length === 0 || !editingNote) return
    
    setUploadingPhotos(true)
    
    try {
      for (let i = 0; i < files.length; i++) {
        const formData = new FormData()
        formData.append('file', files[i])
        
        const response = await fetch(`${API_URL}/api/upload-photo/${editingNote.id}`, {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${token}`
          },
          body: formData,
        })
        
        if (response.ok) {
          const data = await response.json()
          setFormData(prev => ({
            ...prev,
            photos: [...(prev.photos || []), data.filename]
          }))
        }
      }
      
      fetchNotes()
    } catch (error) {
      console.error('Error uploading photos:', error)
    } finally {
      setUploadingPhotos(false)
    }
  }

  const handleDeletePhoto = async (filename) => {
    if (!editingNote || !window.confirm('Delete this photo?')) return
    
    try {
      await fetch(`${API_URL}/api/delete-photo/${editingNote.id}/${filename}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${token}`
        }
      })
      
      setFormData(prev => ({
        ...prev,
        photos: prev.photos.filter(p => p !== filename)
      }))
      
      fetchNotes()
    } catch (error) {
      console.error('Error deleting photo:', error)
    }
  }

  const filteredNotes = notes.filter(note =>
    note.wine_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    note.varietal.toLowerCase().includes(searchTerm.toLowerCase()) ||
    (note.region && note.region.toLowerCase().includes(searchTerm.toLowerCase()))
  )

  const getColorStyle = (color) => {
    const colors = {
      'Red': 'bg-red-100 text-red-800',
      'White': 'bg-yellow-100 text-yellow-800',
      'Rosé': 'bg-pink-100 text-pink-800',
      'Sparkling': 'bg-blue-100 text-blue-800'
    }
    return colors[color] || 'bg-gray-100 text-gray-800'
  }

  // Login Screen
  if (!token) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-purple-900 via-purple-700 to-purple-500 flex items-center justify-center p-4">
        <div className="bg-white rounded-2xl shadow-2xl p-8 max-w-md w-full">
          <div className="text-center mb-8">
            <div className="text-6xl mb-4">🍷</div>
            <h1 className="text-3xl font-bold text-gray-800 mb-2">Wine Notes</h1>
            <p className="text-gray-600">Track your wine tasting journey</p>
          </div>
          
          <form onSubmit={handleDemoLogin} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Email Address
              </label>
              <input
                type="email"
                value={loginEmail}
                onChange={(e) => setLoginEmail(e.target.value)}
                placeholder="your@email.com"
                required
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
              />
            </div>
            
            <button
              type="submit"
              className="w-full bg-purple-600 text-white py-3 rounded-lg hover:bg-purple-700 transition font-semibold"
            >
              Sign In
            </button>
          </form>
          
          <div className="mt-6 text-center text-sm text-gray-500">
            <p>Demo Mode - Just enter any email to continue</p>
            <p className="mt-2 text-xs">Google OAuth ready for production</p>
          </div>
        </div>
      </div>
    )
  }

  // Main App continues... (truncated for length - same as before)
  return (
    <div className="min-h-screen bg-gray-50">
      <div className="bg-gradient-to-r from-purple-900 to-purple-700 text-white py-6 shadow-lg">
        <div className="max-w-7xl mx-auto px-4 flex justify-between items-center">
          <div>
            <h1 className="text-4xl font-bold">🍷 Wine Notes</h1>
            <p className="text-purple-200 mt-2">Your personal wine tasting journal</p>
          </div>
          <button
            onClick={handleLogout}
            className="px-4 py-2 bg-purple-800 hover:bg-purple-900 rounded-lg transition"
          >
            Sign Out
          </button>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 py-8">
        <div className="mb-8 flex gap-4 flex-wrap">
          <input
            type="text"
            placeholder="Search wines..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="flex-1 min-w-[250px] px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
          />
          <button
            onClick={() => setIsFormOpen(true)}
            className="px-6 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition font-semibold"
          >
            + Add Wine Note
          </button>
        </div>

        {filteredNotes.length === 0 ? (
          <div className="text-center py-16">
            <div className="text-6xl mb-4">🍷</div>
            <h3 className="text-xl font-semibold text-gray-700 mb-2">No wine notes yet</h3>
            <p className="text-gray-500">Start tracking your wine journey!</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {filteredNotes.map((note) => (
              <div
                key={note.id}
                className="bg-white rounded-lg shadow-md hover:shadow-lg transition p-6 border border-gray-200"
              >
                <div className="flex justify-between items-start mb-4">
                  <div className="flex-1">
                    <h3 className="text-xl font-bold text-gray-800 mb-1">
                      {note.wine_name}
                    </h3>
                    {note.producer && (
                      <p className="text-sm text-gray-600">{note.producer}</p>
                    )}
                  </div>
                  <span className={`px-3 py-1 rounded-full text-xs font-semibold ${getColorStyle(note.color)}`}>
                    {note.color}
                  </span>
                </div>

                <div className="space-y-2 mb-4 text-sm">
                  <div className="flex justify-between">
                    <span className="text-gray-600">Varietal:</span>
                    <span className="font-medium text-gray-800">{note.varietal}</span>
                  </div>
                  {note.rating && (
                    <div className="flex justify-between items-center">
                      <span className="text-gray-600">Rating:</span>
                      <span className="font-medium text-gray-800">
                        {'⭐'.repeat(Math.floor(note.rating))} {note.rating}/5
                      </span>
                    </div>
                  )}
                </div>

                {note.photos && note.photos.length > 0 && (
                  <div className="mb-4">
                    <div className="grid grid-cols-3 gap-2">
                      {note.photos.map((photo, idx) => (
                        <img
                          key={idx}
                          src={`${API_URL}/uploads/${photo}`}
                          alt="Wine"
                          className="w-full h-20 object-cover rounded-lg cursor-pointer hover:opacity-80 transition"
                          onClick={() => window.open(`${API_URL}/uploads/${photo}`, '_blank')}
                        />
                      ))}
                    </div>
                  </div>
                )}

                <div className="flex gap-2">
                  <button
                    onClick={() => handleEdit(note)}
                    className="flex-1 px-4 py-2 bg-purple-100 text-purple-700 rounded-lg hover:bg-purple-200 transition text-sm font-medium"
                  >
                    Edit
                  </button>
                  <button
                    onClick={() => handleDelete(note.id)}
                    className="flex-1 px-4 py-2 bg-red-100 text-red-700 rounded-lg hover:bg-red-200 transition text-sm font-medium"
                  >
                    Delete
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Form Modal - implementation continues... */}
    </div>
  )
}

export default App
