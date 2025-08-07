# Sample data
people = [
    {"name": "Lexis", "age": 30, "city": "New York"},
    {"name": "Gasper", "age": 28, "city": "Los Angeles"},
    {"name": "Lorick", "age": 35, "city": "Chicago"},
]

# Build table rows dynamically
rows_html = ""
for person in people:
    rows_html += f"""
    <tr>
        <td>{person['name']}</td>
        <td>{person['age']}</td>
        <td>{person['city']}</td>
    </tr>
    """

# Wrap in full table HTML
table_html = f"""
<table>
  <thead>
    <tr>
      <th>Name</th>
      <th>Age</th>
      <th>City</th>
    </tr>
  </thead>
  <tbody>
    {rows_html}
  </tbody>
</table>
"""

# Optional styling
st.markdown("""
<style>
table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 10px;
}
th, td {
  border: 1px solid #ccc;
  padding: 8px;
  text-align: left;
}
thead {
  background-color: #f2f2f2;
}
</style>
""", unsafe_allow_html=True)

# Render table
st.markdown(table_html, unsafe_allow_html=True)