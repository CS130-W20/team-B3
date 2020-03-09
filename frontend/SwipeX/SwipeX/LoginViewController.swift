//
//  LoginViewController.swift
//  SwipeX
//
//  Created by Ashwin Vivek on 2/19/20.
//  Copyright © 2020 CS 130. All rights reserved.
//

import UIKit
import GoogleSignIn
import Alamofire
import SwiftyJSON

class LoginViewController: UIViewController, GIDSignInDelegate {

    @IBOutlet weak var loginButton: UIButton!
    
    override func viewDidAppear(_ animated: Bool) {
        if ((GIDSignIn.sharedInstance()?.hasPreviousSignIn())!) {
            GIDSignIn.sharedInstance()?.restorePreviousSignIn()
        }
    }
    
    @IBAction func prepareForUnwind(segue: UIStoryboardSegue) {

    }
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        // Do any additional setup after loading the view.
        GIDSignIn.sharedInstance()?.presentingViewController = self

        // Automatically sign in the user.
        GIDSignIn.sharedInstance()?.delegate = self
    }
    
    @IBAction func loginAction(_ sender: Any) {
        GIDSignIn.sharedInstance()?.signIn()
    }
    
    func checkIfNewUser(email: String, completion: @escaping (NSDictionary) -> Void) {
        
        let parameters: [String: String] = [
            "email": email
        ]
    AF.request("https://02a6b230.ngrok.io/api/accounts/check/", method:.post, parameters: parameters, encoder: JSONParameterEncoder.default).responseJSON { response in
            switch response.result {
                case .success:
                    if let value = response.value as? NSDictionary {
//                        if let data = value.data(using: String.Encoding.utf8) {
//                            let json = JSON(data)
                        completion(value)
                    }
                case let .failure(error):
                    print(error)
            }
        }
    }
    
    func sign(_ signIn: GIDSignIn!, didSignInFor user: GIDGoogleUser!, withError error: Error!) {
        if let error = error {
           if (error as NSError).code == GIDSignInErrorCode.hasNoAuthInKeychain.rawValue {
             print("The user has not signed in before or they have since signed out.")
           } else {
             print("\(error.localizedDescription)")
           }
           return
        }
        
        // Perform any operations on signed in user here.
        let userId = user.userID                  // For client-side use only!
        let idToken = user.authentication.idToken // Safe to send to the server
        let fullName = user.profile.name
        let givenName = user.profile.givenName
        let familyName = user.profile.familyName
        let email = user.profile.email

        UserDefaults.standard.set(givenName, forKey: "givenName")
        UserDefaults.standard.set(familyName, forKey: "familyName")
        UserDefaults.standard.set(fullName, forKey: "fullName")
        UserDefaults.standard.set(email, forKey: "email")
        
        let storyboard = UIStoryboard(name: "Main", bundle: nil)
        
        checkIfNewUser(email: email!) { response in
            // Do your stuff here
            let userExists = response["exists"] as? String
            
            // user doesn't exist
            if (userExists == "0") {
                let phoneNumberVC = storyboard.instantiateViewController(withIdentifier: "phoneNumberVC")
                phoneNumberVC.modalPresentationStyle = .fullScreen
                
                if ((GIDSignIn.sharedInstance()?.presentingViewController.isBeingPresented)!) {
                    GIDSignIn.sharedInstance()?.presentingViewController.dismiss(animated: true, completion: {
                        self.present(phoneNumberVC, animated: true, completion: nil)
                    })
                    
                } else {
                    self.present(phoneNumberVC, animated: true, completion: nil)
                }
            } else {
                // user does exist
                let userId = response["user_id"] as? Int
                 UserDefaults.standard.set(userId, forKey: "userId")
                let tabbarVC = storyboard.instantiateViewController(withIdentifier: "MainTabBarVC")
                tabbarVC.modalPresentationStyle = .fullScreen
        
                if ((GIDSignIn.sharedInstance()?.presentingViewController.isBeingPresented)!) {
                    GIDSignIn.sharedInstance()?.presentingViewController.dismiss(animated: true, completion: {
                        self.present(tabbarVC, animated: true, completion: nil)
                    })
        
                } else {
                    self.present(tabbarVC, animated: true, completion: nil)
                }
            }
        }
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
