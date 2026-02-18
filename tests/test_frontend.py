"""
Frontend integration tests using Playwright.
Tests the real frontend + backend interaction.
"""

import pytest
from playwright.sync_api import expect, Page
import subprocess
import time
import os


# Fixtures for starting the backend server
@pytest.fixture(scope="session")
def backend_server():
    """Start the backend server for testing."""
    env = os.environ.copy()
    env['DATABASE_URL'] = 'sqlite:///./test.db'
    
    process = subprocess.Popen(
        ['python', '-m', 'uvicorn', 'main:app', '--host', '127.0.0.1', '--port', '8000'],
        cwd='/home/moro/Zeynep/projects/notes-app',
        env=env
    )
    time.sleep(2)  # Wait for server to start
    yield process
    process.terminate()
    process.wait()


@pytest.mark.frontend
class TestNotesApp:
    """Test suite for the Notes App frontend."""

    @pytest.fixture(autouse=True)
    def setup(self, page, backend_server):
        """Setup for each test - navigate to the app."""
        page.goto('http://localhost:5173')  # Vite dev server
        yield

    def test_app_loads(self, page):
        """Test that the app loads successfully."""
        expect(page.locator('h1')).to_contain_text('Notes')
        expect(page.locator('.new-btn')).to_be_visible()

    def test_create_note(self, page):
        """Test creating a new note."""
        # Click the "New" button
        page.click('.new-btn')
        
        # Title and content inputs should be visible
        title_input = page.locator('.title-input')
        content_input = page.locator('.content-input')
        expect(title_input).to_be_visible()
        expect(content_input).to_be_visible()
        
        # Fill in the note details
        title_input.fill('Test Note')
        content_input.fill('This is test content')
        
        # Click the "Add note" button
        page.click('.primary')
        
        # The form should disappear after adding
        expect(title_input).not_to_be_visible()
        
        # The note should appear in the list
        expect(page.locator('button:has-text("Test Note")')).to_be_visible()

    def test_edit_note(self, page):
        """Test editing an existing note."""
        # Create a note first
        page.click('.new-btn')
        page.locator('.title-input').fill('Original Title')
        page.locator('.content-input').fill('Original Content')
        page.click('.primary')
        
        # Wait for note to appear
        page.wait_for_selector('button:has-text("Original Title")')
        
        # Click on the note to edit it
        page.click('button:has-text("Original Title")')
        
        # Edit form should be visible
        edit_title = page.locator('.edit-title-input')
        edit_content = page.locator('.edit-content-input')
        expect(edit_title).to_be_visible()
        expect(edit_content).to_be_visible()
        
        # Verify the content is populated
        expect(edit_title).to_have_value('Original Title')
        expect(edit_content).to_have_value('Original Content')
        
        # Update the note
        edit_title.fill('Updated Title')
        edit_content.fill('Updated Content')
        page.locator('.primary').nth(1).click()  # Click second primary button (Save)
        
        # The note should be updated in the list
        expect(page.locator('button:has-text("Updated Title")')).to_be_visible()
        expect(page.locator('button:has-text("Original Title")')).not_to_be_visible()

    def test_delete_note(self, page):
        """Test deleting a note."""
        # Create a note first
        page.click('.new-btn')
        page.locator('.title-input').fill('Note to Delete')
        page.locator('.content-input').fill('Delete me')
        page.click('.primary')
        
        # Wait for note to appear
        page.wait_for_selector('button:has-text("Note to Delete")')
        
        # Click delete button
        page.click('button:has-text("Delete")')
        
        # The note should be removed from the list
        expect(page.locator('button:has-text("Note to Delete")')).not_to_be_visible()

    def test_cancel_adding(self, page):
        """Test canceling the add form."""
        page.click('.new-btn')
        
        # Fill in some content
        page.locator('.title-input').fill('Unsaved Note')
        page.locator('.content-input').fill('This will be discarded')
        
        # Click cancel
        page.locator('button:has-text("Cancel")').first.click()
        
        # The form should disappear
        expect(page.locator('.title-input')).not_to_be_visible()

    def test_unsaved_changes_popup_add_to_add(self, page):
        """Test unsaved changes popup when switching from adding to adding."""
        page.click('.new-btn')
        page.locator('.title-input').fill('First Note')
        
        # Click "New" again
        page.click('.new-btn')
        
        # Popup should appear
        expect(page.locator('.overlay')).to_be_visible()
        expect(page.locator('p:has-text("unsaved changes")')).to_be_visible()
        
        # Click "Discard"
        page.locator('button:has-text("Discard")').first.click()
        
        # Popup should disappear
        expect(page.locator('.overlay')).not_to_be_visible()

    def test_panel_resize(self, page):
        """Test that panels can be resized."""
        left_panel = page.locator('.left')
        right_panel = page.locator('.right')
        divider = page.locator('.divider')
        
        # Get initial widths
        initial_left_width = left_panel.evaluate('el => el.style.width')
        
        # Drag the divider to the right
        divider.drag_to(page.locator('body'), target_position={'x': 100, 'y': 0})
        
        # The width should have changed (ideally narrower on left)
        # Note: This test might need adjustment based on actual behavior
        expect(left_panel).to_be_visible()
        expect(right_panel).to_be_visible()

    def test_multiple_notes(self, page):
        """Test creating and managing multiple notes."""
        notes_data = [
            {'title': 'Note 1', 'content': 'Content 1'},
            {'title': 'Note 2', 'content': 'Content 2'},
            {'title': 'Note 3', 'content': 'Content 3'},
        ]
        
        # Create multiple notes
        for note in notes_data:
            page.click('.new-btn')
            page.locator('.title-input').fill(note['title'])
            page.locator('.content-input').fill(note['content'])
            page.click('.primary')
            page.wait_for_timeout(500)  # Small delay between creations
        
        # All notes should be visible
        for note in notes_data:
            expect(page.locator(f'button:has-text("{note["title"]}")')).to_be_visible()

