//
//  ParkControllerViewController.swift
//  University Parking
//
//  Created by Thomas Marosz on 11/15/17.
//  Copyright © 2017 PSE. All rights reserved.
//

import UIKit
import MapKit
import Firebase

class ParkControllerViewController: UIViewController, MKMapViewDelegate,
CLLocationManagerDelegate, UITableViewDataSource {
    
    var spaces: [Space] = []
    
    let lotRef = Database.database().reference(withPath: "lots")
    
    var lots = Array<Lot>()
    
    var selectedLot: Lot?
    
    var reserveAnnotation: Bool?
    
    var selectedSpace: Space?
    
    var reservedSpaces = [Space]()
    var reservedSpaceLot: Lot?
    var selectedSpaceLotID: String?
    
    var userPermit = "FV"
    
    var userName = "Vandy Student"
    
    func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        
        if !(ReserveOutlet.currentTitle == "Reserve Spot") {
            return reservedSpaces.count
        } else {
            if (selectedLot == nil) {
                return 0
            } else {
                return selectedLot!.spaces.count
            }
        }
    }
    
    func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        
        let cell = tableView.dequeueReusableCell(withIdentifier: "AvailableSpotCell", for: indexPath)
        
        if !(ReserveOutlet.currentTitle == "Reserve Spot") {
            cell.textLabel!.text = "Reserved Spot: " + reservedSpaces[indexPath.row].getName()
        } else {
            if (selectedLot == nil) {
                cell.textLabel!.text = "No spots available."
            } else {
                cell.textLabel!.text = "Spot: " + selectedLot!.spaces[indexPath.row].getName()
            }
        }
        
        return cell
    }
    
    func tableView(_ tableView: UITableView, didSelectRowAtIndexPath indexPath: IndexPath) {
        
        print("Reached code")
        
        if (ReserveOutlet.currentTitle == "Reserve Spot") {
            selectedSpace = selectedLot?.spaces[indexPath.row]
            //selectedSpaceLotID = selectedLot?.id
        }
    }
    
    
    @IBOutlet weak var mapView: MKMapView!
    @IBOutlet weak var parkingLotsButton: UIBarButtonItem!
    @IBOutlet weak var accountButton: UIBarButtonItem!
    
    @IBOutlet weak var helpButton: UIBarButtonItem!
    
    @IBOutlet weak var ReserveOutlet: UIButton!

    @IBOutlet weak var TableViewOutlet: UITableView!
    
    @IBOutlet weak var ParkButtonOutlet: UIButton!
    
    func mapView(_ mapView: MKMapView, viewFor annotation: MKAnnotation) -> MKAnnotationView? {
        
        if annotation is Lot {
            
            // guard let annotation = annotation as? Lot else { return nil }
            
            let identifier = "lot"
            var view: MKMarkerAnnotationView
            
            if let dequeuedView = mapView.dequeueReusableAnnotationView(withIdentifier: identifier)
                as? MKMarkerAnnotationView {
                dequeuedView.annotation = annotation
                view = dequeuedView
            } else {
                
                view = MKMarkerAnnotationView(annotation: annotation, reuseIdentifier: identifier)
                view.canShowCallout = true
                view.calloutOffset = CGPoint(x: -5, y: 5)
                view.rightCalloutAccessoryView = UIButton(type: .detailDisclosure)
            }
            return view
            
        } else if annotation is Space {
            
            let identifier = "space"
            let view = MKMarkerAnnotationView()

            view.markerTintColor = .cyan

            return view
            
            
        }
        return nil
    }
    
    func mapView(_ mapView: MKMapView, annotationView view: MKAnnotationView, calloutAccessoryControlTapped control: UIControl) {
            TableViewOutlet.reloadData()
        if view.annotation is Lot {
            
            TableViewOutlet.reloadData()
            
            selectedLot = view.annotation as? Lot
            
            TableViewOutlet.reloadData()
            
            TableViewOutlet.isHidden = false
            ReserveOutlet.isHidden = false
            ParkButtonOutlet.isHidden = false
            
        } else if view.annotation is Space {
            
            selectedSpace = view.annotation as! Space
            
            TableViewOutlet.reloadData()
            
        }
        

    }
    
    func mapView(_ mapView: MKMapView, didDeselect view: MKAnnotationView) {
        selectedLot = nil
        selectedSpace = nil
        TableViewOutlet.reloadData()
        
    }
    
    @IBAction func ReserveCancelButton(_ sender: Any) {
        
        if (ReserveOutlet.currentTitle == "Reserve Spot") {
            
            reserveAnnotation = true
            print(selectedLot)
            print(selectedSpace)
            if(selectedSpace != nil) {
            self.mapView.addAnnotation(selectedSpace!)
            selectedSpace?.occupied = true
            reservedSpaces.append(selectedSpace!)
            reservedSpaceLot = selectedLot
                
                editSpace(for: (reservedSpaceLot?.id)!, updatedLot: reservedSpaceLot!)
            
            ReserveOutlet.setTitle("Cancel Reservation", for: .normal)
            ParkButtonOutlet.setTitle("Leave Lot", for: .normal)
            TableViewOutlet.reloadData()
            }
            else {
                let alert = UIAlertController(title: "Error", message: "Select A Space To Reserve", preferredStyle: .alert)
                
                let action = UIAlertAction(title: "OK", style: .default, handler: nil)
                alert.addAction(action)
                self.present(alert, animated: true, completion: nil)
            }
        
        } else {
            print("ReserveCancelButton")
            print("========Did not return true=========")
            
            for annotation in mapView.annotations as [MKAnnotation] {
                if annotation is Space {
                    mapView.removeAnnotation(annotation)
                }
            }
            
            for space in reservedSpaces as [Space] {
                space.occupied = false
                editSpace(for: (reservedSpaceLot?.id!)!, updatedLot: reservedSpaceLot!)
            }
            
            reservedSpaces.removeAll()
            
            ReserveOutlet.setTitle("Reserve Spot", for: .normal)
            ParkButtonOutlet.setTitle("Park Now", for: .normal)
            TableViewOutlet.reloadData()
        }
        
    }
    
    @IBAction func ParkButtonAction(_ sender: Any) {
        
        if (ParkButtonOutlet.currentTitle == "Park Now") {
            
            reserveAnnotation = true
            
            print(selectedLot)
            print(selectedSpace)
            
            if (selectedSpace != nil) {
            self.mapView.addAnnotation(selectedSpace!)
            selectedSpace?.occupied = true
            reservedSpaces.append(selectedSpace!)
            reservedSpaceLot = selectedLot
                editSpace(for: (reservedSpaceLot?.id!)!, updatedLot: reservedSpaceLot!)
            
            ParkButtonOutlet.setTitle("Leave Lot", for: .normal)
            ReserveOutlet.setTitle("Cancel Reservation", for: .normal)
            TableViewOutlet.reloadData()
            }
            else {
                let alert = UIAlertController(title: "Error", message: "Select A Space To Park At", preferredStyle: .alert)
                
                let action = UIAlertAction(title: "OK", style: .default, handler: nil)
                alert.addAction(action)
                self.present(alert, animated: true, completion: nil)
            }
            
        } else {
            print("ParkButtonAction")
            print("========Did not return true=========")
            
            for annotation in mapView.annotations as [MKAnnotation] {
                if annotation is Space {
                    mapView.removeAnnotation(annotation)
                }
            }
            
            for space in reservedSpaces as [Space] {
                space.occupied = false
                editSpace(for: (reservedSpaceLot?.id!)!, updatedLot: reservedSpaceLot!)
            }
            
            reservedSpaces.removeAll()
            
            ParkButtonOutlet.setTitle("Park Now", for: .normal)
            ReserveOutlet.setTitle("Reserve Spot", for: .normal)
            TableViewOutlet.reloadData()
        }
        
    }
    
    let locationManager = CLLocationManager()
    func checkLocationAuthorizationStatus() {
        if CLLocationManager.authorizationStatus() == .authorizedWhenInUse {
            mapView.showsUserLocation = true
        } else {
            locationManager.requestWhenInUseAuthorization()
        }
    }
    
    // https://www.raywenderlich.com/160517/mapkit-tutorial-getting-started
    
    let regionRadius: CLLocationDistance = 1000
    func centerMapOnLocation(location: CLLocation) {
        let coordinateRegion = MKCoordinateRegionMakeWithDistance(location.coordinate,
                                                                  regionRadius, regionRadius)
        mapView.setRegion(coordinateRegion, animated: true)
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    
    func determineCurrentLocation() {
        locationManager.delegate = self
        locationManager.desiredAccuracy = kCLLocationAccuracyBest
        
        if CLLocationManager.locationServicesEnabled() {
            locationManager.startUpdatingLocation()
        }
    }
    
    func getAllLots(success: @escaping ([AnyObject]) -> Void) {
        lotRef.observe(.value, with: { (snapshot) in
            self.lots.removeAll()
            let lotDictionary = snapshot.value as? [String : AnyObject] ?? [:]
            for (key, value) in lotDictionary {
                
                if let oneLot = value as? [String: AnyObject] {
                    
                    //if oneTicket["companyId"] as? String != nil {
                        //if (oneTicket["companyId"] as? String)! == user.getCurrentCompany().getCompanyID() {
                            
                            let tempLot = Lot(title: "")
                            tempLot.id = key
                            tempLot.title = oneLot["title"] as! String
                            let lat = oneLot["lat"] as! Double
                            let long = oneLot["long"] as! Double
                            tempLot.coordinate = CLLocationCoordinate2D(latitude: lat, longitude: long)
                            let permitDictionary = oneLot["permits"] as! Array<String>
                            
                            for value in permitDictionary {
                                tempLot.permit.append(value)
                            }
                            
                    
                            let spacesDictionary = oneLot["spaces"] as! Array<[String: AnyObject]>
                            for oneSpace in spacesDictionary {
                                
                                let lat = lat + 0.001
                                let long = long + 0.001
                                
                                let spaceCoordinate = CLLocationCoordinate2D(latitude: lat, longitude: long)
                                let tempSpace = Space(coordinate: spaceCoordinate, name: oneSpace["name"] as! String, title: oneSpace["name"] as! String, permit: oneSpace["permit"] as! String, lot: tempLot.title, occupied: oneSpace["occupied"] as! Bool, priceRateClass: oneSpace["priceRateClass"] as! String)
                                if !(tempSpace.occupied!) && (tempSpace.permit == self.userPermit) {
                                    tempLot.addSpace(newSpace: tempSpace)
                                }
                                
                            }
                            self.lots.append(tempLot)
                }
            }
           return success(self.lots)
        })
    }
    
    func locationManager(_ manager: CLLocationManager, didUpdateLocations locations: [CLLocation]) {
        let userLocation:CLLocation = locations[0] as CLLocation
        
        let center = CLLocationCoordinate2D(latitude: userLocation.coordinate.latitude, longitude: userLocation.coordinate.longitude)
        let region = MKCoordinateRegion(center: center, span: MKCoordinateSpan(latitudeDelta: 0.01, longitudeDelta: 0.01))
        
        mapView.setRegion(region, animated: true)
        
    }
    
    override func viewDidLoad() {
        super.viewDidLoad()
        checkLocationAuthorizationStatus()
        determineCurrentLocation()
        mapView.delegate = self
        reserveAnnotation = false
        
        getAllLots(success: { (response) in
            self.lots = response as! Array<Lot>
            for object in self.lots {
                self.mapView.addAnnotation(object)
            }
           
        })
        print(spaces)

        
    }
    
    func editSpace(for lotID: String, updatedLot: Lot) {
   
        for i in stride(from: 0, to: updatedLot.spaces.count, by: 1) {
            
            lotRef.child(lotID).child("spaces").child("\(i)").updateChildValues([
                "name": updatedLot.getSpaces()[i].getName(),
                "occupied": updatedLot.getSpaces()[i].getOccupied(),
                "permit": updatedLot.getSpaces()[i].getPermit(),
                "priceRateClass": updatedLot.getSpaces()[i].getPriceClass()
                ])
        }
        
    }
    

}
