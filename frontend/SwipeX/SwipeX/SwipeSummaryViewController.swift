//
//  SwipeSummaryViewController.swift
//  SwipeX
//
//  Created by Ashwin Vivek on 3/12/20.
//  Copyright © 2020 CS 130. All rights reserved.
//

import UIKit
import Alamofire
import SwiftyJSON

class SwipeSummaryViewController: UIViewController, UITableViewDelegate, UITableViewDataSource {
    
    @IBOutlet weak var acceptedBids: UITableView!
    @IBOutlet weak var acceptedAsks: UITableView!
    @IBOutlet weak var pendingBids: UITableView!
    @IBOutlet weak var pendingAsks: UITableView!
    
    var acceptedBidsArray = [NSDictionary]()
    var acceptedSwipesArray = [NSDictionary]()
    var pendingBidsArray = [NSDictionary]()
    var pendingSwipesArray = [NSDictionary]()
    
    override func viewWillAppear(_ animated: Bool) {
        let userId = UserDefaults.standard.integer(forKey: "userId")
               let parameters = [
                   "user_id": userId
               ]
               AF.request("\(NGROK_URL)/api/accounts/user_data/", method:.post, parameters: parameters, encoding:JSONEncoding.default).responseJSON { response in
                   switch response.result {
                       case .success:
                           if let value = response.value as? NSDictionary {
                            let bidsDict = value["Bids"] as? NSDictionary
                            let swipesDict = value["Swipes"] as? NSDictionary
                            
                            self.acceptedBidsArray = bidsDict!["Accepted"] as! [NSDictionary]
                            
                            self.pendingBidsArray = bidsDict!["Pending"] as! [NSDictionary]
                            self.acceptedSwipesArray = swipesDict!["Sold"] as! [NSDictionary]
                            self.pendingSwipesArray = swipesDict!["Available"] as! [NSDictionary]
                            
                            self.pendingBids.reloadData()
                            self.pendingAsks.reloadData()
                            self.acceptedBids.reloadData()
                            self.acceptedAsks.reloadData()
                            
                           }
                       case let .failure(error):
                           print(error)
                   }
               }
    }
    
    override func viewDidLoad() {
        super.viewDidLoad()

        // Do any additional setup after loading the view.
        acceptedAsks.delegate = self
        acceptedAsks.dataSource = self
        acceptedBids.delegate = self
        acceptedBids.dataSource = self
        pendingAsks.delegate = self
        pendingAsks.dataSource = self
        pendingBids.delegate = self
        pendingBids.dataSource = self
        
        pendingAsks.register(informationCell.self, forCellReuseIdentifier: "Ic")
        pendingBids.register(informationCell.self, forCellReuseIdentifier: "Ic")
        acceptedBids.register(informationCell.self, forCellReuseIdentifier: "Ic")
        acceptedAsks.register(informationCell.self, forCellReuseIdentifier: "Ic")
    }
    
    func numberOfSections(in tableView: UITableView) -> Int {
        return 1
    }
    
    func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        if(tableView == self.acceptedAsks) {
            return acceptedSwipesArray.count
        }
        else if(tableView == self.acceptedBids) {
            return acceptedBidsArray.count
        }
        else if(tableView == self.pendingAsks) {
            return pendingSwipesArray.count
        }
        else if(tableView == self.pendingBids) {
            return pendingBidsArray.count
        }
        return 1
    }
    
    func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
    
        let cell = tableView.dequeueReusableCell(withIdentifier: "Ic", for: indexPath) as! informationCell
        
        print(self.pendingBidsArray)
        print(self.pendingSwipesArray)
        print(self.acceptedBidsArray)
        print(self.acceptedSwipesArray)
        
        if(tableView == self.acceptedAsks) {
        //            cell.name =
            cell.name = "John Doe"
            cell.diningHallName = self.acceptedSwipesArray[indexPath.row]["hall_name"] as! String
            cell.price = self.acceptedSwipesArray[indexPath.row]["price"] as! String
            
        }
                else if(tableView == self.acceptedBids) {
            cell.name = "John Doe"
            cell.diningHallName = self.acceptedBidsArray[indexPath.row]["hall_name"] as! String
            cell.price = self.acceptedBidsArray[indexPath.row]["bid_price"] as! String
                }
                else if(tableView == self.pendingAsks) {
            cell.name = "John Doe"
            cell.diningHallName = self.pendingSwipesArray[indexPath.row]["hall_name"] as! String
            cell.price = self.pendingSwipesArray[indexPath.row]["price"] as! String
                }
                else if(tableView == self.pendingBids) {
            cell.name = "John Doe"
            cell.diningHallName = self.pendingBidsArray[indexPath.row]["hall_name"] as! String
            cell.price = self.pendingBidsArray[indexPath.row]["bid_price"] as! String
                }
        
        return cell
        
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
