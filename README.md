# Example Python Repository

This is a collection of python mini-projects that demonstrate how to work with various
Carbon Workspace features. 

To makes sure everything works properly run the following command before getting
started:

```shell
pip install -r requirements.txt
```

## Notebooks

This contains several example Jupyter notebooks that demonstrate the capabilities of 
Jupyter in the Carbon IDE.

## GUI

A simple GUI application that demonstrates how to view the GUI from the desktop. 
After you have started the `simple.py` module. Open the desktop to view the
application's window.

## Server 

This is a simple web API that demonstrates how you can host a server on the Carbon
Workspace and connect to the server. 

To start the server, run the following command:
   
   ```python
   python server/main.py
   ```
   
The server will be listening on port `8080`. To connect to it from your carbon workspace
navigate to the following location in your browser:

```
https://www.graderthan.com/carbon/workspace/wss-<WORKSPACE-ID>/8080/
```

Replace `<WORKSPACE-ID>` with your workspace's actual ID. You can find the ID in the
URL of your running workspace. 

## Assignment

This shows example python assignments and their accompanying unit tests used to grade
the assignments. All the unit tests are ready for use with the Auto-Grader. 
