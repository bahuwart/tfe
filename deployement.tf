
variable "admin_login" {
type = string
}

variable "admin_password" {
type = string
}

resource "proxmox_vm_qemu" "mlavoine-VM20248" {
    name        = "mlavoine-VM20248"
    desc        = "Ubuntu virtual machine of Marc Lavoine"
    vmid        = "20248"
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
        tag    = 20
    }

    serial {
        type = "socket"
        id = 0
    }
    ciuser = var.admin_login
    cipassword = var.admin_password
    ipconfig0   = "ip=10.0.20.248/24,gw=10.0.20.1"
    vm_state = "running"
}


resource "proxmox_vm_qemu" "bhuwart-VM10213" {
    name        = "bhuwart-VM10213"
    desc        = "Ubuntu virtual machine of Basil Huwart"
    vmid        = "10213"
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
    ipconfig0   = "ip=10.0.10.213/24,gw=10.0.10.1"
    vm_state = "running"
}


resource "proxmox_vm_qemu" "bhuwart-VM1087" {
    name        = "bhuwart-VM1087"
    desc        = "Ubuntu virtual machine of Basil Huwart"
    vmid        = "1087"
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
    ipconfig0   = "ip=10.0.10.87/24,gw=10.0.10.1"
    vm_state = "running"
}

