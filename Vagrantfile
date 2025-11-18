# Vagrantfile
# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  
  # 1. Sistema Operativo
  config.vm.box = "ubuntu/jammy64" 
  
  # 2. Mapear puerto de Flask (usando 5001 como puerto de host para evitar colisiones)
  # Aplicación accesible en http://localhost:5001
  config.vm.network "forwarded_port", guest: 5000, host: 5001
  
  # 3. Aprovisionamiento: Ejecuta el Playbook de Ansible
  config.vm.provision "ansible" do |ansible|
    # Especifica que Vagrant debe ejecutar el archivo playbook.yml
    ansible.playbook = "playbook.yml"
    
    # Ejecutar tareas con privilegios de root (sudo)
    ansible.become = true
    
    # Asegura que se ejecuta en el host de la MV
    ansible.limit = "all" 
  end
end