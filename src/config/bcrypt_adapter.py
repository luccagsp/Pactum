import bcrypt

# Password to hash
password = b"xdd"

# Generate a salt
salt = bcrypt.gensalt()
print(salt)
# Hash the password
hashed = bcrypt.hashpw(password, salt)

# Output the hashed password
print(hashed)

#Verify the password

coso = b"xdd"
if bcrypt.checkpw(coso, hashed):
    print("It Matches!")
else:
    print("It Does not Match :(")