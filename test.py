from projectile_object import projectile_object

def main():
    a1 = projectile_object("a1")
    a2 = projectile_object("a2")
 
    a2.sys_params["ang"] = 30

    print(a1.sys_params["ang"])
    print(a2.sys_params["ang"])

if __name__ == "__main__":
    main()