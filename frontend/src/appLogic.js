const API = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export default {
  data() {
    return {
      notes: [],
      newTitle: '',
      newContent: '',
      adding: false,
      editing: false,
      editId: null,
      editTitle: '',
      editContent: '',
      isResizing: false,
      showPopup: -1, /* 0->adding to adding, 1->editing to editing, 2->editing to adding, 3->adding to editing */
      currentNote: null,
      leftWidth: 50,
      rightWidth: 50
    }
  },

  /* When the component loads, it automatically calls fetchNotes() to load all saved notes from backend */
  created() {
    this.fetchNotes()
  },

  methods: {
    /**
     * Fetches all notes from the backend API and updates the notes list.
     * Uses async/await to pause execution until the HTTP request to ${API}/notes resolves.
     */
    async fetchNotes() {
        const res = await fetch(`${API}/notes`)
        this.notes = await res.json()
    },

    /**
     * Initiates the creation of a new note.
     * Checks for unsaved changes before switching to the add form if already adding or editing.
     */
    createNote() {
        /* If you're already in the add form and click "New" again, check for unsaved changes */
        if(this.adding) {
        if(this.newTitle !== '' || this.newContent !== '') {
            this.showPopup = 0
        }
        return
        }
        this.adding = true;

        /* If you're currently editing a note and click "New", check for unsaved changes before switching */
        if(this.editing) {
            if(this.currentNote.title !== this.editTitle || this.currentNote.content !== this.editContent) {
                this.showPopup = 2
            }
            else {
                this.cancelEdit()
            }
            return
        }
    },

    /**
     * Sends a new note to the backend API and refreshes the notes list.
     * Returns early if title is empty. Converts the note object to JSON format for the API request.
     */
    async addNote() {
        if (!this.newTitle) return
        const res = await fetch(`${API}/notes`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ title: this.newTitle, content: this.newContent }) // Converts a JavaScript object into a JSON-formatted string
        })
        
        /* res.ok is true when the HTTP status code is in the 200–299 range */
        if (res.ok) {
            this.cancelAdding()
            await this.fetchNotes()
        } 
        else {
            alert('Failed to create note')
        }
    },

    /**
     * Cancels the add note form and clears all input fields.
     */
    cancelAdding() {
        this.adding = false
        this.newTitle = ''
        this.newContent = ''
    },

    /**
     * Deletes a note by ID from the backend API and refreshes the notes list.
     * HTTP 204 (No Content) status indicates successful deletion with no response body.
     * @param {number} id - The ID of the note to delete
     */
    async deleteNote(id) {
        const res = await fetch(`${API}/notes/${id}`, { method: 'DELETE' })
      
        /* 204 is the special "No Content" status — commonly used to indicate a successful deletion */
        if (res.status === 204) this.fetchNotes()
        this.editing = false
    },

    /**
     * Initiates editing of a note. Checks for unsaved changes when switching between notes or from add to edit mode.
     * @param {Object} n - The note object to edit
     */
    startEdit(n) {
        /* If you're already editing a note and click on another note to edit, check for unsaved changes before switching */
        if(this.editing) {
            if(this.currentNote.title !== this.editTitle || this.currentNote.content !== this.editContent) {
                this.showPopup = 1
                this.currentNote = n
                return
            }
        }
        this.editing = true
        this.currentNote = n
        this.editId = n.id
        this.editTitle = n.title
        this.editContent = n.content

        /* If you're currently adding a new note and click on an existing note to edit, check for unsaved changes */
        if(this.adding) {
            if(this.newTitle !== '' || this.newContent !== '') {
                this.showPopup = 3
            }
            else {
                this.cancelAdding()
            }
            return
        }
    },

    /**
     * Cancels the edit note form and clears the edit state.
     */
    cancelEdit() {
        this.editing = false
        this.editId = null
    },

    /**
     * Sends the edited note to the backend API and refreshes the notes list.
     */
    async updateNote() {
        const res = await fetch(`${API}/notes/${this.editId}`, {
            method: 'PUT',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ title: this.editTitle, content: this.editContent })
        })

        if (res.ok) {
            this.cancelEdit()
            await this.fetchNotes()
        } 
        else {
            alert('Update failed')
        }
    },

    /**
     * Starts the resize operation for the left and right panels.
     */
    startResize() {
        this.isResizing = true
    },

    /**
     * Stops the resize operation for the left and right panels.
     */
    stopResize() {
        this.isResizing = false
    },

    /**
     * Handles the resize event for dynamically adjusting panel widths.
     * Maintains minimum (20%) and maximum (80%) width constraints for the left panel.
     * @param {MouseEvent} e - The mouse event object
     */
    resize(e) {
        if (!this.isResizing) return
        const container = e.currentTarget
        const newLeftWidth = (e.clientX / container.clientWidth) * 100
        if (newLeftWidth > 20 && newLeftWidth < 80) {
            this.leftWidth = newLeftWidth
            this.rightWidth = 100 - newLeftWidth
        }
    }
  }
}
