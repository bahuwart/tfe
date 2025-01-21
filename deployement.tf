
variable "admin_login" {
type = string
}

variable "admin_password" {
type = string
}

resource "proxmox_vm_qemu" "mlavoine-VM20210" {
    name        = "mlavoine-VM20210"
    desc        = "Ubuntu virtual machine of Marc Lavoine"
    vmid        = "20210"
    target_node = "pve"

    agent   = 0
    clone   = "linux-cloud2"
    cores   = 1
    sockets = 1
    cpu     = "host"
    memory  = 1024

    os_type  = "cloud-init"
    scsihw   = "virtio-scsi-pci"
    bootdisk = "scsi0"

    disk {
        type         = "disk"
        storage      = "local-lvm"
        size         = "4G"
        iothread     = true
        slot = "scsi0"
    }

    disk {
        type    = "cloudinit"
        storage = "local-lvm"
        slot = "ide2"
        size = "4M"
    }

    network {
        model  = "virtio"
        bridge = "vmbr3"
        tag    = 20
    }

    serial {
        type = "socket"
        id = 0
    }
    ciuser = var.admin_login
    cipassword = var.admin_password
    ipconfig0   = "ip=10.0.20.210/24,gw=10.0.20.1"
    vm_state = "running"
}


resource "proxmox_vm_qemu" "bhuwart-VM10108" {
    name        = "bhuwart-VM10108"
    desc        = "Ubuntu virtual machine of Basil Huwart"
    vmid        = "10108"
    target_node = "pve"

    agent   = 0
    clone   = "linux-cloud"
    cores   = 1
    sockets = 1
    cpu     = "host"
    memory  = 1024

    os_type  = "cloud-init"
    scsihw   = "virtio-scsi-pci"
    bootdisk = "scsi0"

    disk {
        type         = "disk"
        storage      = "local-lvm"
        size         = "4G"
        iothread     = true
        slot = "scsi0"
    }

    disk {
        type    = "cloudinit"
        storage = "local-lvm"
        slot = "ide2"
        size = "4M"
    }

    network {
        model  = "virtio"
        bridge = "vmbr3"
        tag    = 10
    }

    serial {
        type = "socket"
        id = 0
    }
    ciuser = var.admin_login
    cipassword = var.admin_password
    ipconfig0   = "ip=10.0.10.108/24,gw=10.0.10.1"
    vm_state = "running"
}


resource "proxmox_vm_qemu" "pchaude-VM10155" {
    name        = "pchaude-VM10155"
    desc        = "Ubuntu virtual machine of Patate Chaude"
    vmid        = "10155"
    target_node = "pve"

    agent   = 0
    clone   = "linux-cloud"
    cores   = 1
    sockets = 1
    cpu     = "host"
    memory  = 1024

    os_type  = "cloud-init"
    scsihw   = "virtio-scsi-pci"
    bootdisk = "scsi0"

    disk {
        type         = "disk"
        storage      = "local-lvm"
        size         = "4G"
        iothread     = true
        slot = "scsi0"
    }

    disk {
        type    = "cloudinit"
        storage = "local-lvm"
        slot = "ide2"
        size = "4M"
    }

    network {
        model  = "virtio"
        bridge = "vmbr3"
        tag    = 10
    }

    serial {
        type = "socket"
        id = 0
    }
    ciuser = var.admin_login
    cipassword = var.admin_password
    ipconfig0   = "ip=10.0.10.155/24,gw=10.0.10.1"
    vm_state = "running"
}

