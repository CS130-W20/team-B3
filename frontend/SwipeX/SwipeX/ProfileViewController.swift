//
//  ProfileViewController.swift
//  SwipeX
//
//  Created by Ashwin Vivek on 3/8/20.
//  Copyright © 2020 CS 130. All rights reserved.
//

import UIKit
import GoogleSignIn

class ProfileViewController: UIViewController {

    @IBAction func signOut(_ sender: Any) {
        GIDSignIn.sharedInstance()?.signOut()
        GIDSignIn.sharedInstance()?.disconnect()
        self.performSegue(withIdentifier: "unwindToLoginVC", sender: self)
    }
    
    override func viewDidLoad() {
        super.viewDidLoad()

        // Do any additional setup after loading the view.
    }
    

    /*
    // MARK: - Navigation

    // In a storyboard-based application, you will often want to do a little preparation before navigation
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        // Get the new view controller using segue.destination.
        // Pass the selected object to the new view controller.
    }
    */

}
