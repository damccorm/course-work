//
//  Lot.swift
//  University Parking
//
//  Created by Thomas Marosz on 11/29/17.
//  Copyright © 2017 PSE. All rights reserved.
//

import UIKit
import MapKit

class Lot: NSObject, MKAnnotation {
    var title: String?
    var coordinate: CLLocationCoordinate2D
    var spaces: [Space]
    var permit: [String]
    var id: String!
    
//    init(title: "", coordinate: CLLocationCoordinate2D, spaces: [Space], permit: [String]) {
//        self.title = title
//        self.coordinate = coordinate
//        self.spaces = spaces
//        self.permit = permit
//
//        super.init()
//    }
    
  
    
    init(title: String) {
        self.title = title
        self.coordinate = CLLocationCoordinate2D()
        self.spaces = [Space]()
        self.permit = [String]()
        self.id = ""
        
        super.init()
    }
    
    func setTitle(title: String) {
    self.title = title
    }
    
    func addSpace(newSpace: Space) {
        self.spaces.append(newSpace)
    }
    
    func getSpaces() -> [Space] {
        return self.spaces
    }
    
//    var subtitle: String? {
//        return "Permit: \(permit); Spaces available: \(spaces.count)"
//    }

}
