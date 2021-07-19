import QtQuick 2.15
import QtQuick.Window 2.14
import QtQuick.Controls 2.14
import QtQuick3D 1.15

Window {
    id: window
    width: 1280
    height: 720
    visible: true
    title: "Dynamic Model Creation example"

    Button {
        id: addButton
        anchors.left: parent.left
        anchors.top: parent.top
        anchors.margins: 20
        text: "Add Model"
        implicitWidth: 150

        background: Rectangle {
            implicitWidth: 150
            implicitHeight: 40
            opacity: enabled ? 1 : 0.3
            color: parent.down ? "#6b7080" : "#848895"
            border.color: "#222840"
            border.width: 1
            radius: 5
        }

        onClicked: {
            if (shapeSpawner.instances.length < shapeSpawner.maxInstances)
                shapeSpawner.addOrRemove(true);
        }
    }

    Label {
        id: countLabel
        anchors.top: parent.top
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.margins: 20
        font.pointSize: 20
        font.bold: true
        color: "#848895"
    }

    Button {
        id: removeButton
        anchors.right: parent.right
        anchors.top: parent.top
        anchors.margins: 20
        text: "Remove Model"
        implicitWidth: 150

        background: Rectangle {
            implicitWidth: 150
            implicitHeight: 40
            opacity: enabled ? 1 : 0.3
            color: parent.down ? "#6b7080" : "#848895"
            border.color: "#222840"
            border.width: 1
            radius: 5
        }

        onClicked: {
            if (shapeSpawner.instances.length > 0)
                shapeSpawner.addOrRemove(false);
        }
    }

    View3D {
        anchors.fill: parent
        camera: camera
        renderMode: View3D.Underlay

        environment: SceneEnvironment {
            clearColor: "black"
            backgroundMode: SceneEnvironment.Color
            antialiasingMode: SceneEnvironment.MSAA
            antialiasingQuality: SceneEnvironment.High
        }

        PointLight {
            position: Qt.vector3d(0, 0, 0);
            brightness: 1500
        }

        Node {
            position: Qt.vector3d(0, 0, 0);

            PerspectiveCamera {
                position: Qt.vector3d(0, 0, 600)
            }

            eulerRotation.y: -90

            SequentialAnimation on eulerRotation.y {
                loops: Animation.Infinite
                PropertyAnimation {
                    duration: 5000
                    to: 360
                    from: 0
                }
            }
        }

        Node {
            id: shapeSpawner
            property real range: 300
            property var instances: []
            readonly property int maxInstances: 100

            function addOrRemove(add) {
                if (add) {
                    // Create a new weirdShape at random postion
                    var xPos = (2 * Math.random() * range) - range;
                    var yPos = (2 * Math.random() * range) - range;
                    var zPos = (2 * Math.random() * range) - range;
                    var weirdShapeComponent = Qt.createComponent("WeirdShape.qml");
                    let instance = weirdShapeComponent.createObject(
                            shapeSpawner, { "x": xPos, "y": yPos, "z": zPos,
                                "scale": Qt.vector3d(0.25, 0.25, 0.25)});
                    instances.push(instance);
                    if (instances.length === maxInstances)
                        addButton.enabled = false;
                    else if (instances.length > 0)
                        removeButton.enabled = true;
                } else {
                    // Remove last item in instances list
                    let instance = instances.pop();
                    instance.destroy();
                    if (instances.length === 0)
                        removeButton.enabled = false;
                    else if (instances.length < maxInstances)
                        addButton.enabled = true;
                }
                countLabel.text = "Models in Scene: " + instances.length;
            }
        }

        Component.onCompleted: {
            // Create 10 instances to get started
            for (var i = 0; i < 10; ++i)
                shapeSpawner.addOrRemove(true);
        }
    }
}
