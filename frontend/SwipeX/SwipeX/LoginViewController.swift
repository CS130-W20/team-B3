//
//  LoginViewController.swift
//  SwipeX
//
//  Created by Ashwin Vivek on 2/19/20.
//  Copyright © 2020 CS 130. All rights reserved.
//

import UIKit
import GoogleSignIn

class LoginViewController: UIViewController, GIDSignInDelegate {

    @IBOutlet weak var loginButton: UIButton!
    
    override func viewDidLoad() {
        super.viewDidLoad()

        // Do any additional setup after loading the view.
        GIDSignIn.sharedInstance()?.presentingViewController = self

        // Automatically sign in the user.
        GIDSignIn.sharedInstance()?.restorePreviousSignIn()
        
        GIDSignIn.sharedInstance()?.delegate = self
        
    }
    
    @IBAction func loginAction(_ sender: Any) {
        GIDSignIn.sharedInstance()?.signIn()
    }
    
    func sign(_ signIn: GIDSignIn!, didSignInFor user: GIDGoogleUser!,
                 withError error: Error!) {
        if let error = error {
           if (error as NSError).code == GIDSignInErrorCode.hasNoAuthInKeychain.rawValue {
             print("The user has not signed in before or they have since signed out.")
           } else {
             print("\(error.localizedDescription)")
           }
           return
        }
        
        let storyboard = UIStoryboard(name: "Main", bundle: nil)
        let tabbarVC = storyboard.instantiateViewController(withIdentifier: "MainTabBarVC")
            tabbarVC.modalPresentationStyle = .fullScreen
            GIDSignIn.sharedInstance()?.presentingViewController.dismiss(animated: true, completion: {
                self.present(tabbarVC, animated: true, completion: nil)
            })
       }

       func sign(_ signIn: GIDSignIn!, didDisconnectWith user: GIDGoogleUser!,
                 withError error: Error!) {
         // Perform any operations when the user disconnects from app here.
         // ...
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
