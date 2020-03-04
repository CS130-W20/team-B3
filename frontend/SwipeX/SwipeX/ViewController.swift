//
//  ViewController.swift
//  SwipeX
//
//  Created by Ashwin Vivek on 3/3/20.
//  Copyright © 2020 CS 130. All rights reserved.
//

import UIKit

class ViewController: UIViewController, UICollectionViewDataSource, UICollectionViewDelegate, UICollectionViewDelegateFlowLayout {

    @IBOutlet weak var diningHallCollection: UICollectionView!
    @IBOutlet weak var quickServiceCollection: UICollectionView!
    
    let diningHalls = ["BPlate", "De Neve", "Feast", "Covel"]
    let quickService = ["Cafe 1919", "The Study at Hedrick", "Rendezvous", "BCafe"]
    
    func collectionView(_ collectionView: UICollectionView, numberOfItemsInSection section: Int) -> Int {
        if(collectionView == self.diningHallCollection) {
            return diningHalls.count
        }
        else if (collectionView == self.quickServiceCollection) {
            return quickService.count
        }
        return 0
    }
    
    func collectionView(_ collectionView: UICollectionView,
    layout collectionViewLayout: UICollectionViewLayout,
    sizeForItemAt indexPath: IndexPath) -> CGSize {
        return CGSize(width: 342, height: 226);
    }
    
    func collectionView(_ collectionView: UICollectionView, layout collectionViewLayout: UICollectionViewLayout, insetForSectionAt section: Int) -> UIEdgeInsets {
        return UIEdgeInsets(top: 0, left: 5, bottom: 0, right: 5)
    }
    func collectionView(_ collectionView: UICollectionView, cellForItemAt indexPath: IndexPath) -> UICollectionViewCell {
        let cell = collectionView.dequeueReusableCell(withReuseIdentifier: "Cell", for: indexPath) as! diningHallCell
        if(collectionView == self.diningHallCollection) {
            cell.name.text = diningHalls[indexPath.row]
        }
        else if (collectionView == self.quickServiceCollection) {
            cell.name.text = quickService[indexPath.row]
        }
        cell.image.contentMode = UIView.ContentMode.scaleAspectFill
        cell.layer.borderColor = UIColor.lightGray.cgColor
        cell.layer.borderWidth = 0.1
        cell.layer.shadowColor = UIColor.lightGray.cgColor
        cell.layer.shadowOffset = CGSize(width: 0, height: 6.0)
        cell.layer.shadowRadius = 10
        cell.layer.shadowOpacity = 0.5
        cell.layer.masksToBounds = false
        
        cell.timesAvailable.text = "5-7 pm"
        cell.lowestAsk.text = "$5 lowest ask"
        cell.lowestAsk.adjustsFontSizeToFitWidth = true
        cell.numBids.text = "6 bids"
        
        collectionView.layer.masksToBounds = false
        return cell
    }
    
    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view.
        quickServiceCollection.delegate = self
        quickServiceCollection.dataSource = self
        
        diningHallCollection.delegate = self
        diningHallCollection.dataSource = self
    }


}

