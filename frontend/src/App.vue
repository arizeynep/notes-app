<template>
  <div class="container">
    <h1>Notes</h1>

    <!--@submit.prevent - When you click "Add note", it prevents the page from reloading and calls the createNote() function -->
    <!-- v-model - Two-way binding (whatever you type in the input box gets saved to newTitle and newContent) -->
    <form @submit.prevent="createNote">
      <input v-model="newTitle" placeholder="Title" required />
      <input v-model="newContent" placeholder="Content" />
      <button type="submit">Add note</button>
    </form>

    <ul>
      <li v-for="n in notes" :key="n.id">
        <strong>{{ n.title }}</strong> — {{ n.content }}
        <button @click="deleteNote(n.id)">Delete</button>
        <button @click="startEdit(n)">Edit</button>
      </li>
    </ul>

    <div v-if="editing">
      <h3>Edit</h3>
      <input v-model="editTitle" />
      <input v-model="editContent" />
      <button @click="updateNote">Save</button>
      <button @click="cancelEdit">Cancel</button>
    </div>
  </div>
</template>

<script>

const API = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export default {
  data() {
    return {
      notes: [],
      newTitle: '',
      newContent: '',
      editing: false,
      editId: null,
      editTitle: '',
      editContent: ''
    }
  },

  // When the component loads, it automatically calls fetchNotes() to load all saved notes from backend
  created() {
    this.fetchNotes()
  },

  methods: {
    // async means the function can use await inside it to pause until Promises resolve
    // await pauses execution of this function until the fetch Promise resolves
    // fetch(...) starts an HTTP request to the URL ${API}/notes
    async fetchNotes() {
      const res = await fetch(`${API}/notes`)
      this.notes = await res.json()
    },

    async createNote() {
      if (!this.newTitle) return
      const res = await fetch(`${API}/notes`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ title: this.newTitle, content: this.newContent }) // Converts a JavaScript object into a JSON-formatted string
      })
      
      // res.ok is a shortcut property on the Response object that is true when the HTTP status code is in the 200–299 range
      if (res.ok) {
        this.newTitle = ''
        this.newContent = ''
        await this.fetchNotes()
      } else {
        alert('Failed to create note')
      }
    },

    async deleteNote(id) {
      const res = await fetch(`${API}/notes/${id}`, { method: 'DELETE' })
      
      // 204 is the special "No Content" status — commonly used to indicate a successful deletion where the server returns no body
      if (res.status === 204) this.fetchNotes()
    },

    startEdit(n) {
      this.editing = true
      this.editId = n.id
      this.editTitle = n.title
      this.editContent = n.content
    },

    cancelEdit() {
      this.editing = false
      this.editId = null
    },

    async updateNote() {
      const res = await fetch(`${API}/notes/${this.editId}`, {
        method: 'PUT',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ title: this.editTitle, content: this.editContent })
      })

      if (res.ok) {
        this.cancelEdit()
        await this.fetchNotes()
      } else {
        alert('Update failed')
      }
    }
  }
}
</script>

<style>
.container { max-width: 600px; margin: 2rem auto; font-family: sans-serif; }
input { margin: .25rem; padding: .25rem; }
button { margin-left: .25rem; }
</style>
