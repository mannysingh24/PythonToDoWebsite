from Website import site_setup

website = site_setup()

if __name__ == '__main__': #if I run this file directly
    website.run(debug=True) #run the server(in production you would turn debug off)