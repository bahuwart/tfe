
variable "admin_login" {
type = string
}

variable "admin_password" {
type = string
}

resource "proxmox_vm_qemu" "mlavoine-VM20232" {
    name        = "mlavoine-VM20232"
    desc        = "Ubuntu virtual machine of Marc Lavoine"
    vmid        = "20232"
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
    ipconfig0   = "ip=10.0.20.232/24,gw=10.0.20.1"
    vm_state = "running"
}


resource "proxmox_vm_qemu" "bhuwart-VM1023" {
    name        = "bhuwart-VM1023"
    desc        = "Ubuntu virtual machine of Basil Huwart"
    vmid        = "1023"
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
    ipconfig0   = "ip=10.0.10.23/24,gw=10.0.10.1"
    vm_state = "running"
}


resource "proxmox_vm_qemu" "bhuwart-VM10241" {
    name        = "bhuwart-VM10241"
    desc        = "Ubuntu virtual machine of Basil Huwart"
    vmid        = "10241"
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
    ipconfig0   = "ip=10.0.10.241/24,gw=10.0.10.1"
    vm_state = "running"
}

