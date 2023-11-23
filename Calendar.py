import streamlit as st
from streamlit.components.v1 import components

def main():
    st.title('Calendar in Streamlit')
    
    # HTML code for embedding FullCalendar
    calendar = """
    <div id='calendar'></div>
    <script src="https://cdn.jsdelivr.net/npm/@fullcalendar/core/main.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/@fullcalendar/daygrid/main.min.js"></script>
    <script>
      document.addEventListener('DOMContentLoaded', function() {
        var calendarEl = document.getElementById('calendar');
        var calendar = new FullCalendar.Calendar(calendarEl, {
          plugins: [ 'dayGrid' ], // Use the dayGrid plugin for basic calendar
          initialView: 'dayGridMonth'
          // Other configurations can be added here
        });
        calendar.render();
      });
    </script>
    """

    # Display the calendar
    components.html(calendar, height=600)

if __name__ == "__main__":
    main()


