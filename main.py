import arff 
import io 
import pandas as pd  
import streamlit as st  

st.set_page_config(
    page_title="ARFF/CSV Converter",  # Sets the browser tab title
    page_icon=":floppy_disk:",        # Sets the browser tab icon
)

st.title("ARFF <--> CSV Converter")   # Main title for the app
st.subheader("Easily convert between .arff and .csv formats")  # Secondary header
st.markdown(
    """
    This tool allows you to convert files between **ARFF (Attribute-Relation File Format)** and **CSV (Comma-Separated Values)**.

    - Select the conversion type.
    - Upload a `.arff` or `.csv` file.
    """
)

# Allows user to pick desired conversion direction
conversion_type = st.selectbox("Select conversion type:", ["ARFF to CSV", "CSV to ARFF"])

# Note about general file-format correctness
st.markdown(
    """
    **Note:** Ensure that the uploaded file is in the correct format for conversion.
    """
)

# Lets user upload a file of the specified types
uploaded_file = st.file_uploader("Upload your file", type=["arff", "csv"])

# Checks if a file has been uploaded
if uploaded_file is not None:
    # ARFF to CSV conversion process
    if conversion_type == "ARFF to CSV":
        try:
            content = uploaded_file.read().decode('utf-8')  # Read file content as string
            data = arff.loads(content)                     # Parse ARFF content
            df = pd.DataFrame(
                data['data'], 
                columns=[attr[0] for attr in data['attributes']]  # Extract column names
            )

            st.subheader("🔍 Preview of ARFF Data")
            st.dataframe(df.head())  # Display the first rows of the data

            csv_buffer = io.StringIO()     # Prepare a string buffer for CSV data
            df.to_csv(csv_buffer, index=False)  # Convert dataframe to CSV
            csv_data = csv_buffer.getvalue()    # Retrieve CSV content as string

            st.download_button(
                label="Download CSV",
                data=csv_data,
                file_name=uploaded_file.name.replace(".arff", ".csv"),  # Suggest CSV filename
                mime="text/csv",
            )
            st.success("Converted to CSV successfully!")   # Success message
        except Exception as e:
            st.error(f"Failed to convert ARFF to CSV: {e}")  # Show error on exception

    # CSV to ARFF conversion process
    elif conversion_type == "CSV to ARFF":
        try:
            df = pd.read_csv(uploaded_file)  # Read CSV file into a DataFrame

            st.subheader("🔍 Preview of CSV Data")
            st.dataframe(df.head())  # Display the first rows of the data

            # Define the attributes array based on column types
            attributes = []
            for col in df.columns:
                unique_vals = df[col].dropna().unique()
                if pd.api.types.is_numeric_dtype(df[col]):
                    attributes.append((col, 'REAL'))
                else:
                    attributes.append((col, list(map(str, unique_vals))))

            # Build an ARFF dictionary with relation, attributes, and data
            arff_dict = {
                'description': '',
                'relation': 'converted_data',
                'attributes': attributes,
                'data': df.values.tolist()
            }

            # Write the ARFF data to a string buffer
            arff_buffer = io.StringIO()
            arff.dump(arff_dict, arff_buffer)
            arff_data = arff_buffer.getvalue()

            st.download_button(
                label="Download ARFF",
                data=arff_data,
                file_name=uploaded_file.name.replace(".csv", ".arff"),  # Suggest ARFF filename
                mime="text/plain",
            )
            st.success("Converted to ARFF successfully!")  # Success message
        except Exception as e:
            st.error(f"Failed to convert CSV to ARFF: {e}")  # Show error on exception
