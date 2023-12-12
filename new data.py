# Allow users to input new data
new_data = {
    'School Year': st.number_input('Enter The School Year'),
    'Program ID': st.number_input('Enter The Program ID'),
    'Program Name': st.text_input('Enter The Program Name'),
    'Number of Enrollees': st.number_input('Enter The Number of Enrollees'),
    'Number of Dropout': st.number_input('Enter The Number of Dropout'),
    'Number of Graduates': st.number_input('Enter The Number of Graduates'),
    # Add more inputs for other columns as needed
}

# When a submission button is clicked, append the new data to the DataFrame
if st.button('Add New Data'):
    new_row = pd.DataFrame(new_data, index=[0])
    data = data.append(new_row, ignore_index=True)
    st.success('New data added successfully!')
    
# Save the updated DataFrame back to the CSV file
data.to_csv('data.csv', index=False)