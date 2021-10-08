# RealOptions
Software developed for real options analysis in Python.

# How to run it using Dockerfile <br>
1-) Download the Dockerfile present <a href="https://raw.githubusercontent.com/JohnnyEngineer/RealOptions/main/Dockerfile">here!</a><br>
2-) Open your terminal and type the following command (inside the same folder where the Dockerfile is):<br>
<code>
sudo docker build -t realoptions . -f Dockerfile
</code><br>
3-) After the previous step is completed, type the following command in your terminal:<br>
<code>
sudo xhost local:root && sudo docker run --rm     --network=host --privileged     -v /dev:/dev     -e DISPLAY=$DISPLAY     -v /tmp/.X11-unix:/tmp/.X11-unix     -v $HOME/.Xauthority:/root/.Xauthority     -it realoptions
</code><br>
4-) You should be able to see the software running<br>

# How to run it using Docker public image<br>
<code>
sudo docker run williamsonbrigido/realoptionsapp
</code>
<br>

# How to run it using pip command<br>
Soon..
