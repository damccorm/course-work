//
//  Space.swift
//  University Parking
//
//  Created by Thomas Marosz on 11/30/17.
//  Copyright © 2017 PSE. All rights reserved.
//

import UIKit
import MapKit

class Space: NSObject, MKAnnotation {
    var coordinate: CLLocationCoordinate2D
    var title: String?
    var name: String?
    var permit: String?
    var lot: String?
    var occupied: Bool?
    var priceRateClass: String?
    
    init(coordinate: CLLocationCoordinate2D, name: String?, title: String?, permit: String?, lot: String?, occupied: Bool?, priceRateClass: String?) {
        self.coordinate = coordinate
        self.name = name
        self.title = name
        self.permit = permit
        self.lot = lot
        self.occupied = occupied
        self.priceRateClass = priceRateClass
    }
    
    func getName() -> String  {
        if name != nil {
            return name!
        }
        else {
            return ""
        }
    }
    
    func getOccupied() -> Bool {
        return occupied!
    }
    
    func getPriceClass() -> String {
        return priceRateClass!
    }
    
    func getPermit() -> String {
        return permit!
    }
    var subtitle: String? {
        return lot
    }
    
    var markerTintColor: UIColor  {
        return .cyan
    }
    
}
