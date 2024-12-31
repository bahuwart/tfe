
variable "admin_login" {
type = string
}

variable "admin_password" {
type = string
}

resource "proxmox_vm_qemu" "jdoe" {
    name        = "jdoe-VM"
    desc        = "Ubuntu virtual machine of John Doe"
    vmid        = "2011"
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
        macaddr = "00:22:22:22:22:11"
    }

    serial {
        type = "socket"
        id = 0
    }
    ciuser = var.admin_login
    cipassword = var.admin_password
    ipconfig0   = "ip=dhcp"
    vm_state = "running"
}


resource "proxmox_vm_qemu" "bhuwart" {
    name        = "bhuwart-VM"
    desc        = "Ubuntu virtual machine of Basil Huwart"
    vmid        = "1011"
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
        macaddr = "00:11:11:11:11:11"
    }

    serial {
        type = "socket"
        id = 0
    }
    ciuser = var.admin_login
    cipassword = var.admin_password
    ipconfig0   = "ip=dhcp"
    vm_state = "running"
}


resource "proxmox_vm_qemu" "mlavoine" {
    name        = "mlavoine-VM"
    desc        = "Ubuntu virtual machine of Marc Lavoine"
    vmid        = "2012"
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
        macaddr = "00:22:22:22:22:12"
    }

    serial {
        type = "socket"
        id = 0
    }
    ciuser = var.admin_login
    cipassword = var.admin_password
    ipconfig0   = "ip=dhcp"
    vm_state = "running"
}


resource "proxmox_vm_qemu" "pchaude" {
    name        = "pchaude-VM"
    desc        = "Ubuntu virtual machine of Patate Chaude"
    vmid        = "1012"
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
        macaddr = "00:11:11:11:11:12"
    }

    serial {
        type = "socket"
        id = 0
    }
    ciuser = var.admin_login
    cipassword = var.admin_password
    ipconfig0   = "ip=dhcp"
    vm_state = "running"
}

