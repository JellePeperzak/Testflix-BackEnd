# Open the file in read mode
with open('formattedDriveURLs.txt', 'r') as file:
    content = file.read()

# Replace commas with newlines
content = content.replace(', ', '\n')

# Write the modified content back to the file or a new file
with open('formattedDriveURLs.txt', 'w') as file:
    file.write(content)

print("Commas have been replaced with newlines!")