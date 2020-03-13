//
//  AppDelegate.swift
//  SwipeX
//
//  Created by Ashwin Vivek on 3/3/20.
//  Copyright © 2020 CS 130. All rights reserved.
//

import UIKit
import GoogleSignIn
import Stripe

let NGROK_URL = "https://ad947a9f.ngrok.io"

@UIApplicationMain
class AppDelegate: UIResponder, UIApplicationDelegate {



    func application(_ application: UIApplication, didFinishLaunchingWithOptions launchOptions: [UIApplication.LaunchOptionsKey: Any]?) -> Bool {
        // Override point for customization after application launch.
        GIDSignIn.sharedInstance().clientID = "1093601320222-6htjibr7c3kq9g4f579abcdu1i9h7sql.apps.googleusercontent.com"
        GIDSignIn.sharedInstance()?.hostedDomain = "g.ucla.edu"
        Stripe.setDefaultPublishableKey("pk_test_d3JzWCczi1nb43jv9y1Kpvrg00XSfsIYXE")
        return true
    }

    // MARK: UISceneSession Lifecycle

    func application(_ application: UIApplication, configurationForConnecting connectingSceneSession: UISceneSession, options: UIScene.ConnectionOptions) -> UISceneConfiguration {
        // Called when a new scene session is being created.
        // Use this method to select a configuration to create the new scene with.
        return UISceneConfiguration(name: "Default Configuration", sessionRole: connectingSceneSession.role)
    }

    func application(_ application: UIApplication, didDiscardSceneSessions sceneSessions: Set<UISceneSession>) {
        // Called when the user discards a scene session.
        // If any sessions were discarded while the application was not running, this will be called shortly after application:didFinishLaunchingWithOptions.
        // Use this method to release any resources that were specific to the discarded scenes, as they will not return.
    }


}

