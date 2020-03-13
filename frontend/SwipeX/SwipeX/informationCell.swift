//
//  informationCell.swift
//  SwipeX
//
//  Created by Ashwin Vivek on 3/12/20.
//  Copyright © 2020 CS 130. All rights reserved.
//

import UIKit

class informationCell: UITableViewCell {

    @IBOutlet weak var diningHallNameLabel: UILabel!
    @IBOutlet weak var nameLabel: UILabel!
    @IBOutlet weak var timeLabel: UILabel!
    @IBOutlet weak var priceLabel: UILabel!
    
    var diningHallName:String?
    var name:String?
    var time:String?
    var price:String?
    
    override func awakeFromNib() {
        super.awakeFromNib()
        // Initialization code
        diningHallNameLabel.text = diningHallName
        nameLabel.text = name
        timeLabel.text = time
        priceLabel.text = price
    }

    override func setSelected(_ selected: Bool, animated: Bool) {
        super.setSelected(selected, animated: animated)

        // Configure the view for the selected state
    }
    
    

}
